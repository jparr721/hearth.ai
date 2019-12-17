import re
import json
import urllib.request
import bs4

from bs4 import BeautifulSoup


class PageSummary:
    def __init__(self, url: str):
        """
        Open graph parsers will take data formatted via the open
        graph standard and deliver it for easy consumption

        Parameters
        ----------
        url : str
            This is the URL that will be scraped and analyzer
        """
        self.is_init = False

        if not url.startswith("http") and not url.startswith("https"):
            raise ValueError("Malformed url, please make sure it's a full url")

        self.url = url

    def read(self):
        html = self._fetch_html()
        doc = BeautifulSoup(html, features="html.parser")

        # Page composition is what we use to track all of our parsed info
        self.page_composition = {
            "meta": self._get_meta_info(doc),
            "images": self._get_img(doc),
            "og": self._get_og(doc),
        }

    def _fetch_html(self):
        raw = urllib.request.urlopen(self.url)
        html = raw.read()
        return html

    def _get_meta_info(self, doc: BeautifulSoup):
        title = "".join([t.extract() for t in doc.title])
        description = doc.find("meta", attrs={"name": "description"}).attrs[
            "content"
        ]

        return {"title": title, "description": description}

    def _get_og(self, doc: BeautifulSoup):
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

        def __where(tag: bs4.element.Tag):
            keys = tag.attrs.keys()

            for key in keys:
                if key.startswith("og"):
                    return key

            return None

        meta_tags = doc.find_all("meta")

        # TODO(jparr721) - Optimize this later...
        og_tags = [
            [__where(meta_tag), meta_tag.attrs["content"]]
            for meta_tag in meta_tags
            for key in meta_tag.attrs.keys()
            if key.startswith("og")
        ]

        og_meta = {og[0]: og[1] for og in og_tags}

        return og_meta

    def _get_img(self, doc: BeautifulSoup):
        imgs = [
            {
                "width": img.attrs.get("width", None),
                "height": img.attrs.get("height", None),
                "url": img.attrs.get("src", None),
            }
            for img in doc.find_all("img")
        ]

        return imgs
