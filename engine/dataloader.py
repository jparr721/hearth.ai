from bs4 import BeautifulSoup
from spiders.base import serial_bulk_query, get_robots, read
from spiders.corpus.indexer import Indexer
import re
import sys

regex = re.compile(
    r"^(?:http|ftp)s?://"  # http:// or https://
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
    r"localhost|"  # localhost...
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)


def load_data():
    # Website base host
    base_url = sys.argv[1] if len(sys.argv) > 1 else input("base url: ")

    if not base_url.endswith("/"):
        base_url = base_url + "/"

    # Corpus path to follow
    path_to_follow = sys.argv[2] if len(sys.argv) > 2 else input("follow?: ")

    if path_to_follow.startswith("/"):
        path_to_follow = path_to_follow[1:]

    # Where all the links are to be found
    link_host = sys.argv[3] if len(sys.argv) > 3 else input("host?: ")

    pagination = input("read all pages?: ")

    if pagination != "n" or pagination != "N":
        pagination = True
    else:
        pagination = False

    to_parse = {link_host}

    # If pagination on, hit all the links and scrape the urls down
    if pagination:
        page_data = read(link_host)

        html = BeautifulSoup(page_data, features="html.parser")

        attrs = html.find_all("a")

        pagination_addrs = {
            link.get("href")
            for link in attrs
            if link.get("href") and link.get("href").startswith(link_host)
        }

        to_parse = to_parse.union(pagination_addrs)

    links = []
    for url in to_parse:
        print(f"Parsing url: {url}")
        links.append(get_articles(url, base_url, path_to_follow))

    flat_links = list({y for x in links for y in x})

    # Fire up the indexer
    indexer = Indexer()

    category = input("What is the index category?: ")
    print(f"Using category: {category}")

    # Load the links
    indexer.index_from_list(flat_links, category)

    # Write to disk
    indexer.serialize_index_file(preserve_local_copy=False)
    print("Save complete")


def get_articles(url, base_url, path_to_follow):
    # Read all links to new pages
    html = BeautifulSoup(read(url), features="html.parser")

    # Find all corpus material
    link_addrs = html.find_all("a")

    # Now, filter by the follow path
    article_links = {
        link.get("href")
        for link in link_addrs
        if link.get("href")
        and link.get("href").startswith(f"{base_url}{path_to_follow}")
    }

    return article_links


if __name__ == "__main__":
    load_data()
