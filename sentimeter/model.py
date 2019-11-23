from typing import List

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from sentimeter.corpus import Corpus
from sentimeter.classifier import Classifier
from sentimeter.network import NeuralNetwork, Layer


class TweetModel:

    def __init__(self, corpus: Corpus, classifier: Classifier):
        assert isinstance(corpus, Classifier)
        assert isinstance(classifier, Classifier)
        self._corpus = corpus
        self._classifier = classifier
        self._network = NeuralNetwork([Layer(), Layer(), Layer()])

    def eval(self, text: str) -> int:
        assert False, "Not implemented"

    def train(self, texts: List[str]):
        assert isinstance(texts, list) and all(isinstance(t, str) for t in texts)
        assert False, "Not implemented"
