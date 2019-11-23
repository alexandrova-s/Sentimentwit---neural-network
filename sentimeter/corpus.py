from typing import List

import numpy as np


class Corpus:

    def __init__(self, texts: List[str]):
        assert isinstance(texts, list) and all(isinstance(s, str) for s in texts)

    def to_bag_of_words(self, text: str) -> np.ndarray:
        assert False, "Not implemented"
