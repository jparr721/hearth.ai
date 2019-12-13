from typing import List
from urllib.parse import urlparse

from web_entity import WebEntity


class Node(object):
    def __init__(self, entity: WebEntity, children: List[Node] = None):
        self.entity = entity
        self.children = children
        # Make a lookup dict to easily find child pices.
        if self.children:
            self._children_lookup = {v: i for i, v in enumerate(self.children)}

    @staticmethod
    def parse_node(self, entity: WebEntity):
        pass

    def match_parent_path(self, el_path: str, parent_path: str):
        return el_path.startswith(parent_path)

    def diff_by(self, el_path: str, parent_path: str) -> int:
        """
        Dual iterates two path strings to get the absolute path
        difference via a bijection in the two strings.

        Parameters
        ----------
        el_path : str
            The element path
        parent_path : str
            The path of the parent link
        """
        seq_diff_len = abs(len(el_path) - len(parent_path))

        for i in range(seq_diff_len, len(el_path)):
            pass

    def append_child(self, element: WebEntity):
        pass


class SiteTree(object):
    def __init__(self, root: Node = None):
        self.root = root

    def insert(self, element: Node) -> bool:
        # Parse the URL to read the downstream tree
        parsed_url = urlparse(element.entity.url)

        # Start at root node
        children = self.root.children

        # Cache lookups so they aren't forgotten later
        lookup_cache = []

        # TODO(jparr721) - Change this
        done = False
        while not done:
            for child in children:
                if element in child._children_lookup:
                    return False

                if child.children:
                    # First, see if this is a good spot

                    # Cache the iterator to load it later
                    lookup_cache.append(child.__iter__().next())
                    # Re-assign to queue up anothr look
                    children = child.children
