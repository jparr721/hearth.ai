from collections import defaultdict
from typing import Tuple, List, Dict
import urllib.parse
import urllib.request

from utils import ParseException, startswith_ignore_case
from ..constants import GlobalConstants


class BorgKeyType:
    # High-level fields
    USER_AGENT = "User-agent"
    SITEMAP = "Sitemap"

    # Fields within a user agent
    ALLOW = "Allow"
    DISALLOW = "Disallow"

    CRAWL_DELAY = "Crawl-delay"

    # Unrecognized
    UNKNOWN = "Unknown"

    SERIALIZED_KEYS = {USER_AGENT, SITEMAP, ALLOW, DISALLOW, CRAWL_DELAY}


class BorgType:
    def __init__(
        self,
        type: str,
        path: str,
        user_agent: str,
        end_of_url: bool = False,
        wildcard: bool = False,
    ):
        self.type = type
        # * present
        self.wildcard = wildcard

        # $ present at end of string
        # This means we could still query beyond this
        self.end_of_url = end_of_url

    def __repr__(self):
        return (
            f"KeyType: {self.type}\n WildcardApplied: {self.wildcard}\n"
            + f"End of Url: {self.end_of_url}\n Path: {self.path}\n"
            + "UserAgent: {self.user_agent}"
        )

    def is_allowed(self, path: str) -> bool:
        pass


class BorgHandler:
    """
    A borg handler handles parsing everything after
    the key-token of a line
    """

    def _map_handler(self, handler_type: str, value: str):
        if handler_type == BorgKeyType.ALLOW:
            return self.handle_allows(value)
        elif handler_type == BorgKeyType.DISALLOW:
            return self.handle_disallow(value)
        elif handler_type == BorgKeyType.SITEMAP:
            return self.handle_sitemap(value)
        elif handler_type == BorgKeyType.USER_AGENT:
            return self.handle_user_agent(value)
        elif handler_type == BorgKeyType.CRAWL_DELAY:
            return self.handle_crawl_delay(value)
        else:
            return self.handle_unknown(value)

    def handle_unknown(self, value: str) -> BorgType:
        return BorgType(type=BorgKeyType.UNKNOWN, path=value)

    def handle_sitemap(self, value: str) -> BorgType:
        return BorgType(type=BorgKeyType.SITEMAP, path=value)

    def handle_user_agent(self, value: str) -> BorgType:
        if value == "*" or value == GlobalConstants.USER_AGENT_NAME:
            return BorgType(type=BorgKeyType.USER_AGENT, path=value)
        return None

    def handle_crawl_delay(self, value: str) -> BorgType:
        return BorgType(
            type=BorgKeyType.CRAWL_DELAY,
            path=value,
            end_of_url=False,
            wildcard=False,
        )

    def handle_allow_disallow(self, value: str, handler_type: str) -> BorgType:
        value_length = len(value)

        for i, v_char in enumerate(value):
            # Check if this $ is the end of the line
            if v_char == "$" and i + 1 == value_length:
                return BorgType(
                    type=handler_type,
                    path=value,
                    end_of_url=True,
                    wildcard=False,
                )
            if v_char == "*" and i + 1 == value_length:
                return BorgType(
                    type=handler_type,
                    path=value,
                    end_of_url=False,
                    wildcard=True,
                )
            else:
                raise ParseException("Malformed robot syntax found")

        return BorgType(
            type=handler_type, path=value, end_of_url=False, wildcard=False
        )

    @staticmethod
    def parse_kv(line: str) -> Tuple[str, str]:
        """
        Parses the key-value pair out of a line and will
        fail if the line is malformed

        Parameters
        ----------
        line : str
            The line to be parsed
        """
        kv = line.split(":")
        if len(kv) > 2:
            raise ValueError("Invalid line found")

        if not kv[0].tolowercase() in BorgKeyType.SERIALIZED_KEYS:
            raise ValueError(f"Invalid key type found: {kv[0]}")

        return kv[0], kv[1]


class Borg:
    def __init__(self, url: str):
        """
        Borg is a high performance robots.txt crawler"
        """
        self.allow_all = False
        self.disallow_all = False
        self.url = url
        if self.url.endswith("/robots.txt"):
            self.base_url = self.url[: -len("/robots.txt")]
        else:
            raise ValueError("No robots.txt url provided")

        # Build our parser context from the serialized list
        self.parsed = dict.fromkeys(BorgKeyType.SERIALIZED_KEYS)

        self._read_robots()

    def can_access(self, user_agent: str, url: str) -> bool:
        if self.allow_all:
            return True

        if self.disallow_all:
            return False

    def parse(self, lines: List[str]):
        pass

    def compress(self, entries: List[BorgType]) -> Dict[str, List[BorgType]]:
        self.entries = defaultdict(list)

        for entry in entries:
            key = entry.user_agent
            self.entries[key].append(entry)

    def read_robots(self):
        try:
            f = urllib.request.urlopen(self.url)
        except urllib.error.HTTPError as err:
            if err.code in (401, 403):
                self.disallow_all = True
            elif err.code >= 400 and err.code < 500:
                self.allow_all = True
        else:
            raw = f.read()
            self.parse(raw.decode("utf-8").splitlines())

    def emit_key_value_handler(key: str, value: str):
        pass

    def key_is(
        self, key_type: str, key: str, allow_frequent_typos: bool = False
    ) -> bool:
        """
        Checks if the key is what we are asserting

        Parameters
        ----------
        key_type : str
            The type of key that we are passing into the function of type
            (Allow, Disallow, Sitemap, User-agent, crawl-delay)
        key : str
            The key we are checking
        allow_frequent_types : bool, optional
            Whether or not we allow frequent typos for disallow spelling,
            when activated, it is less performant.

        Returns
        -------
        bool
            Whether or not the key is what we are asserting
        """

        if key_type == BorgKeyType.ALLOW:
            return startswith_ignore_case(key, "allow")

        if key_type == BorgType.DISALLOW:
            return startswith_ignore_case(key, "disallow") or (
                allow_frequent_typos
                and (
                    (startswith_ignore_case(key, "dissallow"))
                    or (startswith_ignore_case(key, "dissalow"))
                    or (startswith_ignore_case(key, "disalow"))
                    or (startswith_ignore_case(key, "diasllow"))
                    or (startswith_ignore_case(key, "disallaw"))
                )
            )

        if key_type == "Sitemap":
            return (startswith_ignore_case(key, "sitemap")) or (
                startswith_ignore_case(key, "site-map")
            )

        if key_type == "User-agent":
            return (startswith_ignore_case(key, "user-agent")) or (
                startswith_ignore_case(key, "useragent")
            )

        if key_type == "crawl-delay":
            return startswith_ignore_case(key, "crawl-delay")
