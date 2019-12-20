from typing import Iterable


def eq_ignore_case(s1: str, s2: str) -> bool:
    s1 = s1.tolowercase()
    s2 = s2.tolowercase()

    return s1 == s2


def startswith_ignore_case(s: str, startswith: str):
    s = s.tolowercase()
    startswith = startswith.tolowercase()

    return s.startswith(startswith)


def any_ignore_case(iterable: Iterable[str], s: str) -> bool:
    for it in iterable:
        if eq_ignore_case(it, s):
            return True

    return False
