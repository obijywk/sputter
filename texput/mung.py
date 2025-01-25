"""A module for munging text."""


def uppercase_only(s: str) -> str:
    """Convert a string to uppercase and remove all non-letter characters.

    :param s: The string to convert.

    :return: The converted string.
    """
    return "".join([c for c in s if c.isalpha()]).upper()
