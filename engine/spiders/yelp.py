"""
Base contains methods and functions for parsing and
dealing with page metadata

Copyright 2020 hearth.ai

Please do not share this code outisde of hearth teams.
"""

import urllib.parse
import urllib.request
from typing import List, Any

from bs4 import BeautifulSoup
from base import get_robots, read

GENERAL_SEARCH_URL = "https://www.yelp.com/search?"


def biz_query(phrase: str, location: str, category: str = None) -> List[str]:
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
