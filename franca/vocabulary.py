from collections import defaultdict
from functools import cached_property, lru_cache
from typing import List, Dict


class Vocabulary:
    def __init__(self):
        self.token_to_index = defaultdict(int)
        self.index_to_token = defaultdict(str)


@cached_property
def serialize_vocabulary(token_to_index: Dict[str, str], add_unk, unk_token):
    return {
        "token_to_index": token_to_index,
        "add_unk": add_unk,
        "unk_token": unk_token,
    }


@cached_property
def from_serialized_vocabulary(contents):
    return serialize_vocabulary(**contents)


def add_token(
    vocabulary: Vocabulary, token: str,
):
    index = vocabulary.token_to_index.get(token, None)

    if not index:
        index = len(vocabulary.token_to_index)
        vocabulary.token_to_index[token] = index
        vocabulary.index_to_token[index] = token

    return index


def add_many_tokens(
    vocabulary: Vocabulary, tokens: str,
):
    return [
        add_token(vocabulary.index_to_token, vocabulary.token_to_index, token)
        for token in tokens
    ]


@lru_cache
def lookup_token(
    index_to_token: Dict[int, str], index: int, unk_token: str = "@"
) -> str:
    if index not in index_to_token:
        return unk_token
    return index_to_token[index]


@lru_cache
def lookup_index(token_to_index: Dict[str, int], token: int) -> str:
    if token not in token_to_index:
        raise KeyError(f"Token {token} is not in the provided Vocabulary")
    return token_to_index[token]


def stringify_vocabulary(mapping: Dict[str, int] or Dict[int, str]):
    return f"<Vocabulary(size={len(mapping)})>"
