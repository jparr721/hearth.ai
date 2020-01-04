import numpy as np
import pandas as pd

from functools import cached_property
from typing import List, Dict, Tuple
from vocabulary import lookup_token, add_token, Vocabulary, SequenceVocabulary


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
    df: pd.DataFrame, X: str, target: str
) -> Tuple[Dict[int, str]]:
    words_vocab = Vocabulary()
    classification_vocab = Vocabulary()

    max_word_length = 0

    for i, r in df.iterrows():
        max_word_length = max(max_word_length, len(r[X]))

        for letter in r[X]:
            add_token(words_vocab, letter)
        add_token(classification_vocab, r[target])

    return (words_vocab, classification_vocab)


def vectorize_sequence_string(
    associated_vocab: SequenceVocabulary, input_string: str, vector_length=-1,
) -> Tuple[List[str], List[str]]:
    """
    Vectorize a string into a vector of observations and targets

    Parameters
    ----------
    input_string : str
        The input string to be vectorized
    vector_length : int
        The argument which forces the length of the index vector

    Returns
    -------
        Tuple[from_vector, to_vector]
    """
    indices = [associated_vocab.begin_seq_index]
    indices.extend(
        associated_vocab.lookup_token(token) for token in input_string
    )
    indices.append(associated_vocab.end_seq_index)

    if vector_length < 0:
        vector_length = len(indices) - 1

    from_vector = np.empty(vector_length, dtype=np.int64)
    from_indices = indices[:-1]
    from_vector[: len(from_indices)] = from_indices
    from_vector[len(from_indices) :] = associated_vocab.mask_index

    to_vector = np.empty(vector_length, dtype=np.int64)
    to_indices = indices[1:]
    to_vector[: len(to_indices)] = to_indices
    to_vector[len(to_indices) :] = associated_vocab.mask_index

    return from_vector, to_vector
