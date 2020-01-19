import os
import sys

from spiders.base import (
    get_robots,
    read,
    concurrent_bulk_query,
    concurrent_batch_process_page_data,
)
from spiders.corpus.indexer import Indexer
from spiders.corpus.fetcher import (
    serial_parse_reader_view,
    unwrap_context_and_extract,
)

KNOWN_OPTS = ["reader"]


def arg_parser(argv):
    relevant_args = argv[1:]

    argument = relevant_args[0]

    if argument not in KNOWN_OPTS:
        print("Arg not found!")
        sys.exit(1)

    if argument == "reader":
        run_reader()


def run_reader():
    # Load our indexer
    indexer = Indexer()

    # Deserialize base file into itself
    indexer.deserialize_index_file()

    # Now, run the query system
    linkdata = indexer.mass_indexer_query_by_category("churches")

    parsed = concurrent_batch_process_page_data(linkdata)

    reader = serial_parse_reader_view(parsed)

    context = unwrap_context_and_extract(reader, "words")

    print(context)


if __name__ == "__main__":
    run_reader()
