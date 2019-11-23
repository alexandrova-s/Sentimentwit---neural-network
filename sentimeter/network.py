from typing import List, Iterable

import numpy as np

from sentimeter.utils import grouper


class Layer:

    def __init__(self, size=3, activation=(lambda x: x, lambda x: np.ones(x.shape))):
        assert isinstance(activation, tuple) and all(callable(f) for f in activation)
        self._size = size
        self._activation, self._derivative = activation

    def __len__(self):
        return self._size

    def __call__(self, *args, **kwargs):
        return self._activation(*args, *kwargs), self._derivative(*args, *kwargs)


class NeuralNetwork:

    def __init__(self, layers: List[Layer]):
        assert isinstance(layers, list) and all(isinstance(l, Layer) for l in layers)
        assert len(layers) > 1
        self._layers = layers
        self._weights = [np.random.rand(len(l2), len(l1) + 1) for l1, l2 in zip(layers[:-1], layers[1:])]

    def propagate(self, x: np.ndarray) -> np.ndarray:
        assert x.ndim == 1
        assert len(x) == len(self._layers[0])

        current_output, _ = self._layers[0](x)
        for weights, layer in zip(self._weights, self._layers[1:]):
            current_output = np.append(current_output, 1)  # bias
            current_output = np.matmul(weights, current_output)
            current_output, _ = layer(current_output)

        return current_output

    def test(self, x_set: List[np.ndarray], yd_set: List[np.ndarray]):
        error = 0.0

        for x, yd in zip(x_set, yd_set):
            diff = self.propagate(x) - yd
            error += 0.5 * diff * diff

        return error / len(x_set)

    def _train_batch(self, x_batch: Iterable[np.ndarray], yd_batch: Iterable[np.ndarray], step: float):

        input_size = len(self._layers[0])
        output_size = len(self._layers[-1])

        # accumulated difference between expected and calculated output
        error = np.zeros((output_size,))
        # accumulated outputs of each layer
        outputs = [np.zeros((len(layer),)) for layer in self._layers]
        # accumulated derivatives of activations of each layer
        activations_derivatives = [np.zeros((len(layer),)) for layer in self._layers]

        batch_size = 0

        for x, yd in zip(x_batch, yd_batch):
            assert x.ndim == 1
            assert yd.ndim == 1
            assert len(x) == input_size
            assert len(yd) == output_size

            batch_size += 1

            # feed-forward accumulating outputs, derivatives of each layer

            output, activation_derivative = self._layers[0](x)
            outputs[0] += output
            activations_derivatives[0] += activation_derivative

            for i in range(1, len(self._layers)):
                weights = self._weights[i - 1]
                layer = self._layers[i]
                output = np.append(output, 1)  # bias
                output = np.matmul(weights, output)
                output, activation_derivative = layer(output)
                outputs[i] += output
                activations_derivatives[i] += activation_derivative

            error += (output - yd)

        error /= batch_size
        outputs = [output / batch_size for output in outputs]
        activations_derivatives = [derivative / batch_size for derivative in activations_derivatives]

        batch_error = 0.5 * np.sum(error * error)

        # Back-propagate

        for i in reversed(range(1, len(self._layers))):
            error = error * activations_derivatives[i]
            weights_derivative = np.outer(error, np.append(outputs[i - 1], 1))
            error = np.matmul(np.transpose(self._weights[i - 1]), error)[:-1]

            self._weights[i - 1] -= weights_derivative * step

        return batch_error

    def train(self, x_set: List[np.ndarray], yd_set: List[np.ndarray], steps: List[float], batch_size: int = 1):
        assert 1 <= batch_size, "Invalid batch size"
        assert len(steps) > 0, "At least one epoch required"

        for epoch_no, step in enumerate(steps):
            assert step > 0.0, "Step has to be positive"

            epoch_error = 0

            for batch_no, batch in enumerate(zip(grouper(batch_size, x_set), grouper(batch_size, yd_set))):
                x_batch, yd_batch = batch
                batch_error = self._train_batch(x_batch, yd_batch, step)
                # print(f"batch {batch_no + 1} -> error {batch_error}")
                epoch_error += batch_error

            print(f"epoch {epoch_no + 1} -> step {step} -> error {epoch_error}")


