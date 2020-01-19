"""
The fetcher does mass fetching of a list of links by
category and returns the derived text corpus
"""

import bs4
import concurrent.futures
import logging
import multiprocessing
from typing import Dict, List

from bs4 import BeautifulSoup
from ..base import concurrent_bulk_query, concurrent_batch_process_page_data
from ..utils import eq_ignore_case
from nltk import sent_tokenize, wordpunct_tokenize, download

download("punkt")


logger = logging.getLogger(__name__)
TAGS = ["h1", "h2", "h3", "h4", "h5", "h6", "h7", "p"]


def serial_parse_reader_view(
    parsed: Dict[str, BeautifulSoup]
) -> Dict[str, List[str]]:
    reader_view = {
        url: [element.text for element in html.find_all(TAGS)]
        for url, html in parsed.items()
    }

    return reader_view


def concurrent_parse_reader_view(
    parsed: Dict[str, BeautifulSoup]
) -> Dict[str, List[str]]:
    worker_count = multiprocessing.cpu_count()

    reader_view = {}

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=worker_count
    ) as executor:
        # Begin thead matching
        futures = {
            executor.submit([element for element in html.find_all(TAGS)]): url
            for url, html in parsed.items()
        }

        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            try:
                data = future.result()
            except Exception as e:
                reader_view[url] = None
                logger.info(f"{url} raised an exception: {e}")
            else:
                reader_view[url] = data

    return reader_view


def unwrap_context_and_extract(
    structured_reader_view: Dict[str, List[str]], unwrap_returns="sentences"
) -> List[str]:
    """
    Unwraps the context of a piece of structured reader view data
    and spits out raw tokens of type sentence or word

    Parameters
    ----------
    structured_reader_view : Dict[str, List[str]]
        The url-indexed reader view content
    unwrap_returns : str, optional possible: ('words', 'sentences'),
    default: 'sentences'
        What return type we'll be delivering
    """
    ret = []

    for _, textlist in structured_reader_view.items():
        for text in textlist:
            for sentence in sent_tokenize(text):
                ret.append(sentence)

    if eq_ignore_case("words", unwrap_returns):
        newret = []
        for sentence in ret:
            for token in wordpunct_tokenize(sentence):
                newret.append(token)
        return newret

    return ret
