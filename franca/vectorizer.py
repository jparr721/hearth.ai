import numpy as np
import pandas as pd

from collections import defaultdict
from functools import cached_property
from typing import List, Dict, Tuple
from vocabulary import lookup_token, add_token, Vocabulary


@cached_property
def one_hot_vectorize1d(
    index_to_token: Dict[int, List[str]], word: str
) -> np.array:
    one_hot = np.zeros(len(index_to_token), dtype=np.float32)

    for token in word:
        one_hot[lookup_token(index_to_token, token)] = 1

    return one_hot


@cached_property
def one_hot_vectorize2d(
    index_to_token: Dict[int, List[str]], word: str, max_word_length: str
) -> np.array:
    one_hot_shape = (len(index_to_token), max_word_length)
    one_hot_matrix = np.zeros(one_hot_shape, dtype=np.float32)

    for pos, c in enumerate(word):
        c_index = lookup_token(index_to_token, c)
        one_hot_matrix[c_index][pos] = 1

    return one_hot_matrix


@cached_property
def vectorize_dataframe(
    df: pd.DataFrame, words_col: str, classification_col: str
) -> Tuple[Dict[int, str]]:
    words_vocab = Vocabulary()
    classification_vocab = Vocabulary()

    max_word_length = 0

    for i, r in df.iterrows():
        max_word_length = max(max_word_length, len(r[words_col]))

        for letter in r[words_col]:
            add_token(words_vocab, letter)
        add_token(classification_vocab, r[classification_col])

    return (words_vocab, classification_vocab)
