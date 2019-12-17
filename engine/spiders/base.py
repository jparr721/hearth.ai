import logging
import urllib.robotparser
from typing import List, Any


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

        self.logger.info("Loading robots.txt")
        self.rp = urllib.robotparser.RobotFileParser()
        self.rp.set_url(f"{self.url}/robots.txt")
        self.rp.read()
        self.logger.info("robots.txt loaded")

    def read(self):
        html = urllib.request.urlopen(self.url)
        html = html.read()
        return html

    def list_query(self, url_list: List[str]) -> List[Any]:
        raise NotImplementedError("Please implement list_query")
