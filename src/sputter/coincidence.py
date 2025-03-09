"""A module implementing index of coincidence calculations."""

from sputter.mung import uppercase_only

__ORD_A = ord("A")


def index_of_coincidence(text: str) -> float:
    """Calculate the index of coincidence for a given text.

    The index of coincidence is a measure of the randomness of a text.
    The higher the index of coincidence, the less random the text.

    :param text: The text for which to calculate the index of coincidence.
    :return: The index of coincidence.
    """
    text = uppercase_only(text)
    n = len(text)
    if n < 2:
        return 26.0
    freq = [0] * 26
    for c in text:
        freq[ord(c) - __ORD_A] += 1
    return 26 * sum(f * (f - 1) for f in freq) / (n * (n - 1))


def delta_bar(text: str, modulus: int) -> float:
    """Calculate the delta bar for a given text and modulus (column count).

    The higher the delta bar, the less random the text when split into modulus columns.

    :param text: The text for which to calculate the delta bar.
    :param modulus: The modulus to use for the delta bar calculation.
    :return: The delta bar index of coincidence.
    """
    text = uppercase_only(text)
    iocs = []
    for i in range(modulus):
        s = "".join(text[j + i] for j in range(0, len(text) - i, modulus))
        iocs.append(index_of_coincidence(s))
    return sum(iocs) / modulus
