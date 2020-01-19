"""
opengraph contains utilities for parsing open graph
search data
"""

import urllib.parse
import urllib.request
from typing import List, Dict
from ..constants import GlobalConstants

from bs4 import BeautifulSoup
from base import (
    get_robots,
    read,
    serial_bulk_query,
    concurrent_batch_process_page_data,
    city_name_to_latlong
)

BASE_URL = "https://google.com/maps"
GENERAL_SEARCH_URL = f"{BASE_URL}/maps/search/"
SUB_SEARCH_URL = f"{BASE_URL}/maps/place"

def knowledge_graph_list(
    phrase: str, location: str, with_root: bool = True
) -> List[str]:
    """
    KNowledge Graph queries Google's knowledge graph location engine
    and finds relevant review data for a given search field for location
    based review data

    Parameters
    ----------
    phrase : str
        The location query phrase
    location : str
        The location we are querying around

    Returns
    -------
    List[str]
        The list of businesses to query
    """
    # Get robots.txt to calivate requests
    robots = get_robots("https://www.google.com/robots.txt")

    if not robots.can_fetch(GlobalConstants.USER_AGENT_NAME_TEST, GENERAL_SEARCH_URL):
        raise LookupError("Url is restricted from scraping")

    lat, long = city_name_to_latlong(location)
    place = urllib.parse.quote_plus(phrase)
    location_string = f"@{','.join((lat, long))}"

    compiled_url = f"{GENERAL_SEARCH_URL}{location_string}"
