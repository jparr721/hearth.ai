"""
Base contains methods and functions for parsing and
dealing with page metadata

Copyright 2020 hearth.ai

Please do not share this code outisde of hearth teams.
"""

import bs4
import concurrent.futures
import logging
import geopy.geocoders import Nominatim
import multiprocessing
import time
import urllib.robotparser

from bs4 import BeautifulSoup
from typing import List, Dict, Any, Tuple
from ..constants import GlobalConstants


logger = logging.getLogger(__name__)


def get_robots(url: str):
    """
    Parses a robots.txt file and returns the created instance

    Parameters
    ----------
    url : str
        The url of the robots file

    Returns
    -------
    RobotFileParser
        The robot file parser instance
    """
    logger.info("Loading robots.txt")
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(url)
    rp.read()
    logger.info("robots.txt loaded")

    return rp


def read(url: str, timeout: int = 30):
    html = urllib.request.urlopen(url, timeout=timeout)
    html = html.read()

    return html


def serial_bulk_query(url_list: List[str], delay: int = None) -> List[Any]:
    return {url: read(url) for url in url_list if time.sleep(delay) is None}


def concurrent_bulk_query(
    url_list: List[str], delay: int = None
) -> Dict[str, str]:
    # Get our number of threads
    worker_count = multiprocessing.cpu_count()

    # Our page cache
    loaded = {}

    # Build our thread pool
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=worker_count
    ) as executor:
        # Begin thread matching
        futures = {
            # read(url=url, timeout=30)
            executor.submit(read, url, 30): url
            for url in url_list
        }

        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            try:
                data = future.result()
            except Exception as e:
                loaded[url] = None
                logger.info(f"{url} made an exception: {e}")
            else:
                loaded[url] = data

    return loaded


def serial_batch_process_page_data(
    page_data: Dict[str, str]
) -> Dict[str, BeautifulSoup]:
    return {
        url: BeautifulSoup(html, features="html.parser")
        for url, html in page_data.items()
    }


def concurrent_batch_process_page_data(
    page_data: Dict[str, str]
) -> Dict[str, BeautifulSoup]:
    # Get our number of threads
    worker_count = multiprocessing.cpu_count()

    # Our process cache
    parsed = {}

    # Build our thread pool
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=worker_count
    ) as executor:
        # Begin thread matching
        kwargs = {"features": "html.parser"}
        futures = {
            executor.submit(BeautifulSoup, html, **kwargs): url
            for url, html in page_data.items()
        }

        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            try:
                data = future.result()
            except Exception as e:
                parsed[url] = None
                logger.info(f"{url} made an exception: {e}")
            else:
                parsed[url] = data

    return parsed


def make_summary(doc: BeautifulSoup):
    return {
        "meta": get_meta_info(doc),
        "images": get_img(doc),
        "og": get_og(doc),
    }


def get_meta_info(doc: BeautifulSoup):
    title = "".join([t.extract() for t in doc.title])
    description = doc.find("meta", attrs={"name": "description"}).attrs[
        "content"
    ]

    return {"title": title, "description": description}


def get_og(doc: BeautifulSoup):
    """
    Gets the metadata from the open graph parser

    Parameters
    ----------
    doc : BeautifulSoup
        The beautiful soup parsed document

    Returns
    -------
    dict
        Dict of open graph tags and their content
    """

    def _where(tag: bs4.element.Tag):
        keys = tag.attrs.keys()

        for key in keys:
            if key.startswith("og"):
                return key

        return None

    meta_tags = doc.find_all("meta")

    # TODO(jparr721) - Optimize this later...
    og_tags = [
        [_where(meta_tag), meta_tag.attrs["content"]]
        for meta_tag in meta_tags
        for key in meta_tag.attrs.keys()
        if key.startswith("og")
    ]

    og_meta = {og[0]: og[1] for og in og_tags}

    return og_meta


def get_img(doc: BeautifulSoup):
    imgs = [
        {
            "width": img.attrs.get("width", None),
            "height": img.attrs.get("height", None),
            "url": img.attrs.get("src", None),
        }
        for img in doc.find_all("img")
    ]

    return imgs

def city_name_to_latlong(name: str) -> Tuple[str, str]:
    geolocator = Nominatim(user_agent=GlobalConstants.USER_AGENT_NAME)

    location = geolocator.geocode(name)

    return location.latitude, location.longitude
