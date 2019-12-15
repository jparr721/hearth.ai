import logging
import requests
from requests.exceptions import ConnectionError

from borg import Borg
from utils import RobotsNotFoundException


class Base:
    def __init__(self, url: str):
        """
        Destroy all websites.

        Parameters
        ----------
        url : str
            The url of the website to begin parsing
        """
        self.logger = logging.getLogger(__name__)
        self.url = url

    def parse_robots(self):
        try:
            r = requests.get(f"{self.url}/robots.txt")
            if r.status_code != 200:
                raise RobotsNotFoundException("No robots.txt file found")

            # Split robots on new line
            robots = [line for line in r.text.split("\n")]

            self.borg = Borg(robots)

        except ConnectionError:
            self.logger.error("Failed to fetch url")
            raise ConnectionError("Invalid Url Supplied")
