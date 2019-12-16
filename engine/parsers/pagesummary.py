import re
import json
import urllib
import bs4

from bs4 import BeautifulSoup


class OpenGraph:
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

        if not url.startswith("http") or not url.startswith("https"):
            raise ValueError("Malformed url, please make sure it's a full url")

        def read(self):
            html = self._fetch_html(url)
            doc = BeautifulSoup(html)

            # Page composition is what we use to track all of our parsed info
            self.pageComposition = {
                "meta": self._get_meta_info(doc),
                "images": self._get_img(doc),
                "og": self._get_og(doc),
            }

        def _fetch_html(self, url: str):
            raw = urllib.request.urlopen(url)
            html = raw.read()
            return html

        def _get_meta_info(doc: BeautifulSoup):
            title = doc.find("title")
            description = doc.find("meta", attrs={"name": "description"})

            return {"title": title, "description": description}

        def _get_og(doc: BeautifulSoup):
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
            imgs = [{"width": img.attrs.get("width", None), "height": img.attrs.get("height", None), "url": img.attrs.get("src", None)} for img in doc.find_all("img")]

            return imgs
