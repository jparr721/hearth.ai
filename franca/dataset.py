import json

import pandas as pd
from sklearn.model_selection import train_test_split
from torch.data import Dataset
from typing import Dict
from vectorizer import vectorize_row


class DatasetGenerator(Dataset):
    def __init__(
        self,
        df: pd.DataFrame,
        vectorizer: Dict[str, int],
        max_seq_len: int,
        test_size: float = 0.3,
        validation_size: float = 0.5,
    ):
        """
        DatasetGenerator is a PyTorch-enabled dataset which can
        interact with its surrounding runtime natively and switch
        context on-the-fly

        Parameters
        ----------
        df : pd.DataFrame
            The pandas dataframe of raw csv data
        vectorizer : Dict[str, int]
            The vectorizer instance of k,v lookups
        max_seq_len : int
            Length of the longest word sequence in the dataset
        """
        self.df = df
        self.vectorizer = vectorizer
        self.max_seq_len = max_seq_len
        self.test_size = test_size if test_size < 1 else test_size / 100
        self.validation_size = (
            validation_size if validation_size < 1 else validation_size / 100
        )

        self.train_df, i = train_test_split(df, test_size=self.test_size)
        self.val_df, self.test_df = train_test_split(
            i, test_size=self.validation_size
        )

        self.lookup_dict = {
            "train": (self.train_df, len(self.train_df)),
            "test": (self.test_df, len(self.test_df)),
            "val": (self.val_df, len(self.val_df)),
        }

        self.set_split("train")

    def set_split(self, split="train"):
        self.target_split = split
        self.target_df, self.target_size = self.lookup_dict[split]

    def __len__(self):
        return self.target_size

    def __getitem__(self, index: int):
        """
        PyTorch dataset item getter

        Parameters
        ----------
        index : int
            The index of the datapoint
        """
        row = self.target_dc.iloc[index]


def find_max_sequence(
    df: pd.DataFrame, col: str, with_unknowns: bool = 2
) -> int:
    return (
        max(map(len, df[col])) + 2 if with_unknowns else max(map(len, df[col]))
    )
