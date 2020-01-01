"""
Yelp contains custom routines for parsing the yelp
search engine

Copyright 2020 hearth.ai

Please do not share this code outisde of hearth teams.
"""

import urllib.parse
import urllib.request
from typing import List, Dict

from bs4 import BeautifulSoup
from base import (
    get_robots,
    read,
    serial_bulk_query,
    concurrent_batch_process_page_data,
)

BASE_URL = "https://www.yelp.com"
GENERAL_SEARCH_URL = f"{BASE_URL}/search?"


def biz_query(
    phrase: str, location: str, category: str = None, with_root: bool = True
) -> List[str]:
    """
    Biz Query queries yelp's biz search engine and scrapes the
    returned list of businesses, returning a list of sub-businesses
    to query further

    Parameters
    ----------
    phrase : str
        The query phrase to enter into the search engine
    location : str
        The location that the query phrase should be localized to
    category : str, optional
        Apply a category to the query

    Returns
    -------
    List[str]
        The list of sub-businesses of a given query and area
    """
    # Get robots.txt to validate requests
    robots = get_robots("https://www.yelp.com/robots.txt")

    if not robots.can_fetch("Googlebot", GENERAL_SEARCH_URL):
        raise LookupError("Url is restricted from scraping")

    # Hit search with url encoded criteria
    find_desc = f"find_desc={urllib.parse.quote_plus(phrase)}"
    find_loc = f"find_loc={urllib.parse.quote_plus(location)}"

    params = [find_desc, find_loc]

    if category:
        cflt = f"cflt={urllib.parse.quote_plus(category)}"
        params.append(cflt)

    # Initiate query
    compiled_url = GENERAL_SEARCH_URL + "&".join(params)
    print("searching: ", compiled_url)

    # Return results
    html = read(compiled_url)

    # Parse the results
    parsed = BeautifulSoup(html, features="html.parser")

    # Find all <a /> tags where href.startswith('/biz')
    biz_links = [
        link.attrs.get("href")
        for link in parsed.find_all("a")
        if link.attrs.get("href", None)
        and link.attrs.get("href").startswith("/biz")
    ]

    if with_root:
        biz_links = [BASE_URL + link for link in biz_links]

    return biz_links


def read_reviews(parsed: BeautifulSoup) -> Dict[str, str]:
    if not parsed:
        return {}

    review_stars = [
        potential_review_stars.attrs.get("aria-label")
        for potential_review_stars in parsed.find_all("div")
        if potential_review_stars.attrs.get("aria-label", None)
        and potential_review_stars.attrs.get("aria-label").endswith(
            "star rating"
        )
    ]

    reviews = [
        review.text
        for review in parsed.find_all("span")
        if review.attrs.get("lang", None) and review.get("lang") == "en"
    ]

    return {review: stars for stars, review in zip(review_stars[1:], reviews)}


if __name__ == "__main__":
    biz_links = biz_query("churches", "Denver")

    print("loading pages")
    loaded_pages = serial_bulk_query(biz_links, 0.1)

    print("parsing pages")
    parsed_pages = concurrent_batch_process_page_data(loaded_pages)

    review_pages = {}

    for url, data in parsed_pages.items():
        review_pages[url] = read_reviews(data)

    print(review_pages)
