"""A module for inserting spaces into unspaced text."""

from typing import List, Optional, Tuple

from sputter.fitness import WordStatistics


def space(
    s: str,
    top_n: Optional[int] = 10,
    ws: Optional[WordStatistics] = None,
    state_size_limit: int = 2048,
) -> List[Tuple[str, float]]:
    """Insert spaces into unspaced text.

    :param s: The unspaced text. Must only contain uppercase letters.
    :param top_n: The number of results to return.
    :param ws: A WordStatistics object. If None, one will be constructed.
    :param state_size_limit: The maximum number of states to keep in memory.

    :return: A list of tuples, where each tuple contains a spaced text and its score.
    """
    if ws is None:
        ws = WordStatistics()

    type StateList = List[Tuple[float, List[str]]]

    states: StateList = [(0.0, [])]

    for c in s:
        new_states: StateList = []
        for score, state in states:
            if state:
                new_words = state[:-1] + [state[-1] + c]
                new_score = (
                    score
                    + ws.word_log_prob(state[-1], True)
                    - ws.word_log_prob(new_words[-1], True)
                )
                new_states.append((new_score, new_words))
            new_states.append((score - ws.word_log_prob(c, True), state + [c]))
        states = sorted(new_states)[:state_size_limit]

    return [(" ".join(words), score) for score, words in states[:top_n]]


def space_with_enumeration(s: str, enumeration: List[int]) -> str:
    """Insert spaces into unspaced text using an enumeration.

    :param s: The unspaced text. Must only contain uppercase letters.
    :param enumeration: A list of integers, where each integer is the number of letters in a word.
    :return: The spaced text.

    :raises ValueError: If the sum of the enumeration does not equal the length of the text.
    """
    if sum(enumeration) != len(s):
        raise ValueError(
            "The sum of the enumeration must equal the length of the text."
        )
    words = []
    for i in enumeration:
        words.append(s[:i])
        s = s[i:]
    return " ".join(words)
