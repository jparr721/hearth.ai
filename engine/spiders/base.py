import logging
import requests
from requests.exceptions import ConnectionError


class Base:
    def __init__(self, url: str):
        """
        Destroy all websites.
        """
        self.logger = logging.getLogger(__name__)
        self.url = url
        self.allow = []
        self.disallowed = []

    def parse_robots(self):
        try:
            r = requests.get(f"{self.url}/robots.txt")
            if r.status_code != 200:
                self.logger.error("No robots file found")

            # Split robots on new line
            robots = [line for line in r.text.split("\n")]

            # Catch allows
            allows = "Allows:"
            self.allows = [line for line in robots if line[0:len(allows)] == allows]

            # Catch disallowed


        except ConnectionError:
            self.logger.error("Failed to fetch url")
            raise ConnectionError("Invalid Url Supplied")
