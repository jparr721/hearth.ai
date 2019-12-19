import unittest

from ..base import Base as b


class TestBase(unittest.TestCase):
    def test_make_summary(self):
        page_composition = b.make_summary("https://www.google.com")
        actual = page_composition
        comp = {
            "meta": {
                "title": "Google",
                "description": "Search the world's information, including webpages, images, videos and more. Google has many special features to help you find exactly what you're looking for.",
            },
            "images": [
                {
                    "width": "272",
                    "height": "92",
                    "url": "/images/branding/googlelogo/1x/googlelogo_white_background_color_272x92dp.png",
                }
            ],
            "og": {},
        }
        self.assertEqual(actual, comp)
