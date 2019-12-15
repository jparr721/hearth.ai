from enum import Enum
from typing import Tuple

from utils import any_ignore_case, ignore_case_eq, startswith_ignore_case


class BorgKeyType(Enum):
    # High-level fields
    USER_AGENT = 0x01
    SITEMAP = 0x02

    # Fields within a user agent
    ALLOW = 0x03
    DISALLOW = 0x04

    # Unrecognized
    UNKNOWN = 0x80


class BorgType:
    def __init__(
        self, type: str, end_of_url: bool = False, wildcard: bool = False
    ):
        self.type = type
        # * present
        self.wildcard = wildcard

        # $ present at end of string
        # This means we could still query beyond this
        self.end_of_url = end_of_url

    def __repr__(self):
        return f"KeyType: {self.type}\n WildcardApplied: {self.wildcard}"


class BorgHandler:
    def __init__(self):
        """
        A borg handler handles parsing everything after
        the key-token of a line
        """
        self.accepted_keys = {
            "allow": 0,
            "disallow": 1,
            "user-agent": 2,
            "crawl-delay": 3,
            "sitemap": 4,
        }

    def handle_allows(self, value: str):
        value_length = len(value)
        parsed = []

        for i, v_char in enumerate(value):
            # Check if this $ is the end of the line
            if v_char == "$" and i + 1 == value_length:
                return BorgType(
                    )

    @staticmethod
    def parse_kv(self, line: str) -> Tuple[str, str]:
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

        if not self._validate_key(kv[0]):
            raise ValueError(f"Invalid key type found: {kv[0]}")

        return kv[0], kv[1]


    def _validate_key(self, key: str) -> bool:
        return any_ignore_case(self.accepted_keys.keys(), key)


class Borg:
    def __init__(self):
        """
        Borg is a high performance robots.txt crawlwer"
        """
        self.allow_frequent_typos = True
        self.allow = []
        self.disallow = []
        self.user_agent = []

    @staticmethod
    def emit_key_value_handler(line, key, value):
        pass

    @staticmethod
    def key_is(self, key_type: str, key: str):
        if key_type == "Allow":
            return startswith_ignore_case(key, "allow")

        if key_type == "Disallow":
            return startswith_ignore_case(key, "disallow") or (
                self.allow_frequent_typos
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

    @staticmethod
    def matches(path: str, pattern: str) -> bool:
        """
        matches a given line with a given path and pattern
        via a regex-based parsing scheme

        Parameters
        ----------
        path : str
            The path of the resource

        Returns
        -------
        bool
            Returns whether or not a given line matches
        """
        pass
