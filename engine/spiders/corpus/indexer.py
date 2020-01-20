import json
import os
from typing import List
from ..base import serial_bulk_query


class Indexer:
    """
    The indexer tool keeps track of lists of files for
    use when scraping very large datasets, works natively
    with dicts to get json output

    Parameters
    ----------
    index_file : str
        The root index file to cache the stuff to
    """

    def __init__(
        self,
        local_index={}
        index_file=f"{os.path.dirname(os.path.realpath(__file__))}/indexed.json",
    ):
        self.index_file = index_file

        if not isinstance(local_index, dict):
            raise ValueError(f"expected index of type 'dict', got '{type(local_index)}'")

        self.local_index = local_index

    def __repr__(self):
        print(f"out_file: {self.index_file}\n index: {repr(self.local_index)}")

    def index_from_list(self, records, category) -> None:
        if category in self.local_index:
            self.local_index[category].extend(records)
        else:
            self.local_index[category] = records

    def index(self, links, category) -> None:
        if category in self.local_index:
            self.local_index[category].extend(links)
        else:
            self.local_index[category] = links

    def deserialize_index_file(self) -> None:
        with open(self.index_file, "r") as f:
            self.local_index = json.load(f)

    def serialize_index_file(self, preserve_local_copy=False) -> None:
        with open(self.index_file, "a") as f:
            json.dump(self.local_index, f)

            if not preserve_local_copy:
                self.local_index = {}
