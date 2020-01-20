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
    raw_corpus_to_frequency_vector,
    mass_indexer_query_by_category,
)


def run_reader(category: str):
    # Load our indexer
    indexer = Indexer()

    # Deserialize base file into itself
    indexer.deserialize_index_file()

    # Now, run the query system
    linkdata = mass_indexer_query_by_category(category)

    parsed = concurrent_batch_process_page_data(linkdata)

    reader = serial_parse_reader_view(parsed)

    context = unwrap_context_and_extract(reader, "words")

    frequency_vector = raw_corpus_to_frequency_vector(context)


if __name__ == "__main__":
    category = sys.argv[1] if len(sys.argv) > 1 else None

    if not category:
        raise ValueError("Gimme an indexer category!")

    run_reader(category)
