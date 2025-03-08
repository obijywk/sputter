"""A module for munging text."""

import random
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
    return re.sub(r"\s+", " ", s)


def randomly_swap_letters(s: str) -> str:
    """Randomly swap two characters in the input string.

    :param s: The string in which to swap characters. Must have length of at least two.

    :return: A new string, with two letters swapped.
    """
    i, j = sorted(random.sample(range(len(s)), 2))
    return s[:i] + s[j] + s[i + 1 : j] + s[i] + s[j + 1 :]
