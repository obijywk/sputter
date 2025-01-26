"""A module for munging text."""

import re


def uppercase_only(s: str) -> str:
    """Convert a string to uppercase and remove all non-letter characters.

    :param s: The string to convert.

    :return: The converted string.
    """
    return "".join([c for c in s if c.isalpha()]).upper()


def uppercase_and_spaces_only(s: str) -> str:
    """Convert a string to uppercase and remove all non-letter, non-space characters.

    :param s: The string to convert.

    :return: The converted string.
    """
    s = "".join([c for c in s if c.isalpha() or c.isspace()]).upper()
    s = re.sub(r"\s+", " ", s)
    return s
