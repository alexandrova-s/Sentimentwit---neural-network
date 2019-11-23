np.random.seed(0)

x_teach = np.random.rand(10000)
x_check = np.random.rand(1000)

y_teach = np.sin(x_teach) / x_teach
y_check = np.sin(x_check) / x_check

n = sn.NeuralNetwork([sn.Layer(1), sn.Layer(5, activation=(np.tanh, lambda x: np.ones(x.shape) - np.square(np.tanh(x)))), sn.Layer(1)])

epochs = 3
step = 0.01

n.train([np.array((x,)) for x in x_teach], [np.array((y,)) for y in y_teach], [0.01, 0.001, 0.0001], 100)

print(f"check set error {n.test([np.array((x,)) for x in x_check], [np.array((y,)) for y in y_check])}")
