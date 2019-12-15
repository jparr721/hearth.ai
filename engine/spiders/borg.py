from typing import Tuple, List

from utils import ParseException, startswith_ignore_case


class BorgKeyType:
    def __init__(self):
        # High-level fields
        self.USER_AGENT = "User-agent"
        self.SITEMAP = "Sitemap"

        # Fields within a user agent
        self.ALLOW = "Allow"
        self.DISALLOW = "Disallow"

        self.CRAWL_DELAY = "Crawl-delay"

        # Unrecognized
        self.UNKNOWN = "Unknown"

    @staticmethod
    def to_serializable(self):
        """
        Returns a serialized set of the class properties
        """
        return {
            self.USER_AGENT,
            self.SITEMAP,
            self.ALLOW,
            self.DISALLOW,
            self.CRAWL_DELAY,
        }


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


class Borg:
    def __init__(self, robots: List[str]):
        """
        Borg is a high performance robots.txt crawlwer"
        """
        self.allow = []
        self.disallow = []
        self.user_agent = []

    @staticmethod
    def emit_key_value_handler(line, key, value):
        pass

    @staticmethod
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

        if key_type == "Allow":
            return startswith_ignore_case(key, "allow")

        if key_type == "Disallow":
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


class BorgHandler:
    """
    A borg handler handles parsing everything after
    the key-token of a line
    """

    def handle_allows(self, value: str):
        value_length = len(value)

        for i, v_char in enumerate(value):
            # Check if this $ is the end of the line
            if v_char == "$" and i + 1 == value_length:
                return BorgType(
                    type="allows", path=value, end_of_url=True, wildcard=False
                )
            if v_char == "*" and i + 1 == value_length:
                return BorgType(
                    type="allows", path=value, end_of_url=False, wildcard=True
                )
            else:
                raise ParseException("Malformed robot syntax found")

        return BorgType(
            type="allows", path=value, end_of_url=False, wildcard=False
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
        return key.tolowercase() in BorgKeyType.to_serializable()
