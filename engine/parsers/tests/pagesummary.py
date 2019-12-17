import unittest

from ..pagesummary import PageSummary


class TestPageSummary(unittest.TestCase):
    page_summary = PageSummary("https://www.google.com")

    def test_constructor(self):
        self.assertRaises(ValueError, PageSummary, "website.com")

    def test_read(self):
        self.page_summary.read()
        actual = self.page_summary.page_composition
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

    def test_html(self):
        summary = PageSummary("http://www.blankwebsite.com/")
        out = summary._fetch_html()
        comp = b'\r\n\r\n<HTML>\r\n<HEAD>\r\n<TITLE>Blank website. Blank site. Nothing to see here.</TITLE>\r\n<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=iso-8859-1">\r\n<META NAME="keywords" CONTENT="blankwebsite, blank website">\r\n<META NAME="description" CONTENT="This resource is provided as a free service for those patrons looking for nothing.">\r\n<META NAME="Author" CONTENT="DLC Websites 1999-2019 - http://www.dlcwebsites.com">\r\n<META NAME="Copyright" CONTENT="DLC Websites 1999-2019 - http://www.dlcwebsites.com - online tools and entertainment">\r\n<meta name="viewport" content="width=device-width, initial-scale=1">\r\n<LINK rel=\'stylesheet\' type=\'text/css\' href=\'sitestyle.css\'>\r\n</HEAD>\r\n\r\n<BODY BGCOLOR="#FFFFFF">\r\n<P>&nbsp;</P>\r\n<P>&nbsp;</P>\r\n<P>&nbsp;</P>\r\n<P>&nbsp;</P>\r\n<P>&nbsp;</P>\r\n<P>&nbsp;</P>\r\n<P>&nbsp;</P>\r\n<P>&nbsp;</P>\r\n<P>&nbsp;</P>\r\n<P>&nbsp;\r\n<div style="margin: 0px auto; width: 95%; height: 90px; max-width: 728px;">\r\n\r\n<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>\r\n<!-- 1Page Responsive -->\r\n<ins class="adsbygoogle"\r\n     style="display:block"\r\n     data-ad-client="ca-pub-7472547808115475"\r\n     data-ad-slot="8787180545"\r\n     data-ad-format="auto"></ins>\r\n<script>\r\n(adsbygoogle = window.adsbygoogle || []).push({});\r\n</script>\r\n\r\n</div>\r\n &nbsp;\r\n \r\n \r\n \r\n \r\n </P>\r\n<P>&nbsp;</P>\r\n<P>&nbsp;</P>\r\n<P>&nbsp;</P>\r\n<P>&nbsp;</P>\r\n<P>&nbsp;</P>\r\n<P>&nbsp;</P>\r\n<P>&nbsp;</P>\r\n<P>&nbsp;</P>\r\n<P>&nbsp;</P>\r\n<P>&nbsp;</P>\r\n<P>&nbsp;</P>\r\n<P>&nbsp;</P>\r\n<P>&nbsp;</P>\r\n<P>&nbsp;</P>\r\n<P>&nbsp;</P>\r\n<P>&nbsp;<B><A href="http://www.pointlesssites.com/">Over 1,000 Pointless Sites</A></B></P>\r\n<P><DIV style="PADDING-BOTTOM: 10px; PADDING-LEFT: 10px; PADDING-RIGHT: 10px; PADDING-TOP: 10px" id=socialmediabuttons>\r\n<TABLE style="MARGIN-LEFT: auto; MARGIN-RIGHT: auto" border=0 cellPadding=2>\r\n<TBODY>\r\n<TR>\r\n<TD style="PADDING-TOP: 7px"><A class=addthis_button_facebook_like fb:like:layout="button_count"></A></TD>\r\n<TD><A class=addthis_button_tweet></A></TD>\r\n<TD><A class=addthis_button_google_plusone g:plusone:size="medium"></A></TD>\r\n<TD><A class="addthis_counter addthis_pill_style"></A></TD></TR></TBODY></TABLE>\r\n<SCRIPT type=text/javascript src="http://s7.addthis.com/js/250/addthis_widget.js#pubid=ra-4fd5fb8f3ab1b3a9"></SCRIPT>\r\n<!-- AddThis Button END --></DIV></P>\r\n</BODY>\r\n</HTML>\r\n'
        self.assertEqual(out, comp)
