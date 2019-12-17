import urllib.parse
import urllib.request
from typing import List, Any

from base import Base


class YelpSpider(Base):
    def __init__(self):
        super().__init__("https://yelp.com")

    def biz_query(self, phrase: str, location: str, category: str = None):
        # Hit search with url encoded criteria
        find_desc = urllib.parse.quote_plus(phrase)
        find_loc = urllib.parse.quote_plus(location)
        cflt = urllib.parse.quote_plus(category) if category else None

        # Return results

        # Find all <a /> tags where href.startswith('/biz')

    def list_query(self, url_list: List[str]) -> List[Any]:
        pass
