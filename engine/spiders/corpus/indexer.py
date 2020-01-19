import json
import os
from urllib.parse import urlparse
from collections import defaultdict
from typing import List
from ..base import serial_bulk_query, get_robots


class IndexerRecord:
    def __init__(self, category: str, links: List[str]):
        self.category = category
        self.links = links


class Indexer:
    """
    The indexer tool keeps track of lists of files for
    use when scraping very large datasets

    Parameters
    ----------
    index_file : str
        The root index file to cache the stuff to
    """

    def __init__(
        self,
        index_file=f"{os.path.dirname(os.path.realpath(__file__))}/indexed.json",
    ):
        self.index_file = index_file
        self.local_index = {}

    def __repr__(self):
        print(f"out_file: {self.index_file}\n index: {repr(self.local_index)}")

    def index_from_list(self, records, category) -> None:
        if category in self.local_index:
            self.local_index[category].extend(records)
        else:
            self.local_index[category] = records

    def index(self, record: IndexerRecord) -> None:
        if record.category in self.local_index:
            self.local_index[record.category].extend(record.links)
        else:
            self.local_index[record.category] = record.links

    def deserialize_index_file(self) -> None:
        with open(self.index_file, "a") as f:
            self.local_index = json.load(f)

    def serialize_index_file(self, preserve_local_copy=False) -> None:
        with open(self.index_file, "a") as f:
            json.dump(self.local_index, f)

            if not preserve_local_copy:
                self.local_index = defaultdict(list)

    def mass_indexer_query_by_category(self, category: str) -> List[str]:
        if not self.local_index:
            raise AttributeError("Local index is empty")

        links = self.local_index[category]

        return serial_bulk_query(links)
