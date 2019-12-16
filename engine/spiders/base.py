import logging
import urllib.robotparser


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

        self.rp = urllib.robotparser.RobotFileParser()
        self.rp.set_url(f"{self.url}/robots.txt")
        self.rp.read()
