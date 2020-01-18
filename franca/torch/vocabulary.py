from collections import defaultdict
from functools import lru_cache
from typing import Dict


class Vocabulary:
    def __init__(self, unk_token: str = "@", token_to_idx=None):
        self.unk_token = unk_token
        self.token_to_index = (
            token_to_idx if token_to_idx else defaultdict(int)
        )
        self.index_to_token = defaultdict(str)

    def serialize(self):
        return {
            "token_to_index": self.token_to_index,
            "unk_token": self.unk_token,
        }

    @classmethod
    def from_serialized(cls, contents):
        return cls(**contents)

    def __len__(self):
        return len(self.token_to_index)

    def __str__(self):
        return f"<Vocabulary(size={len(self)})>"

    def add_token(
        self, token: str,
    ):
        index = self.token_to_index.get(token, None)

        if not index:
            index = len(self.token_to_index)
            self.token_to_index[token] = index
            self.index_to_token[index] = token

        return index

    def add_many_tokens(
        self, tokens: str,
    ):
        return [
            self.add_token(self.index_to_token, self.token_to_index, token)
            for token in tokens
        ]

    @lru_cache
    def lookup_token(
        self, index_to_token: Dict[int, str], index: int, unk_token: str = "@"
    ) -> str:
        if index not in index_to_token:
            return unk_token
        return index_to_token[index]

    @lru_cache
    def lookup_index(self, token_to_index: Dict[str, int], token: int) -> str:
        if token not in token_to_index:
            raise KeyError(f"Token {token} is not in the provided Vocabulary")
        return token_to_index[token]


class SequenceVocabulary(Vocabulary):
    def __init__(
        self,
        unk_token="@",
        mask_token="<MASK>",
        begin_seq_token="<BEGIN>",
        end_seq_token="<END>",
    ):
        super(SequenceVocabulary, self).__init__(unk_token)

        self.mask_token = mask_token
        self.unk_token = unk_token
        self.begin_seq_token = begin_seq_token
        self.end_seq_token = end_seq_token

        self.mask_index = self.add_token(self, self.mask_token)
        self.unk_index = self.add_token(self, self.unk_token)
        self.begin_seq_index = self.add_token(self, self.begin_seq_token)
        self.end_seq_index = self.add_token(self, self.end_seq_token)

    def serialize(self):
        return {
            "unk_token": self.unk_token,
            "mask_token": self.mask_token,
            "begin_seq_token": self.begin_seq_token,
            "end_seq_token": self.end_seq_token,
        }

    @classmethod
    def from_serialized(cls, contents):
        return cls(**contents)
