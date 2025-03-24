import bisect
from dataclasses import dataclass
from typing import List, Optional, Tuple

from sputter.alphabet_trie import AlphabetTrieNode
from sputter.fitness import WordStatistics


def anagram_word(
    letters: str, ws: Optional[WordStatistics] = None
) -> List[Tuple[str, float]]:
    """Return single words that can be formed from the given letters."""

    @dataclass
    class State:
        """A state in the anagram search."""

        word_letters: List[str]
        """The word formed so far."""

        remaining_letters: List[str]
        """The letters remaining to be used."""

        node: AlphabetTrieNode
        """The current node in the trie."""

    if ws is None:
        ws = WordStatistics()

    states = [State([], list(letters), ws.trie())]
    results: List[Tuple[str, float]] = []
    words_found = set()
    while states:
        state = states.pop()
        for i, c in enumerate(state.remaining_letters):
            child = state.node.subtrie(c)
            if child is not None:
                word_letters = state.word_letters + [c]
                if len(state.remaining_letters) == 1 and child.value:
                    word = "".join(word_letters)
                    if word not in words_found:
                        words_found.add(word)
                        results.append((word, child.value))
                else:
                    states.append(
                        State(
                            word_letters,
                            state.remaining_letters[:i]
                            + state.remaining_letters[i + 1 :],
                            child,
                        )
                    )
    return sorted(results, key=lambda t: -t[1])


__ALLOWED_SINGLE_LETTER_WORDS = {"A", "I"}


def anagram_phrase(
    letters: str,
    top_n: Optional[int] = 10,
    ws: Optional[WordStatistics] = None,
    state_size_limit: int = 65536,
    minimum_word_score: Optional[float] = -15.0,
) -> List[Tuple[List[str], float]]:
    """Return phrases that can be formed from the given letters."""

    @dataclass
    class State:
        """A state in the anagram search."""

        words: List[str]
        """The complete words formed so far."""

        words_score: float
        """The total score of the words formed so far."""

        current_word: str
        """The current word being formed so far."""

        remaining_letters: List[str]
        """The letters remaining to be used."""

        node: AlphabetTrieNode
        """The current node in the trie."""

        def current_score(self) -> float:
            """Return the score of the current state."""
            assert self.node.max_descendant_value is not None
            return -self.words_score - self.node.max_descendant_value

    if ws is None:
        ws = WordStatistics()

    states = [State([], 0.0, "", list(letters), ws.trie())]
    results: List[Tuple[List[str], float]] = []
    states_visited = set()
    while states:
        state = states.pop(0)

        visit_key = (
            tuple(sorted(state.words + [state.current_word])),
            tuple(sorted(state.remaining_letters)),
        )
        if visit_key in states_visited:
            continue
        states_visited.add(visit_key)

        assert state.node.max_descendant_value is not None
        if (
            top_n
            and len(results) >= top_n
            and state.words_score + state.node.max_descendant_value < results[-1][1]
        ):
            continue

        for i, c in enumerate(state.remaining_letters):
            child = state.node.subtrie(c)
            if child is not None:
                current_word = state.current_word + c
                remaining_letters = (
                    state.remaining_letters[:i] + state.remaining_letters[i + 1 :]
                )
                if (
                    child.value
                    and (
                        minimum_word_score is None or child.value >= minimum_word_score
                    )
                    and (
                        len(current_word) >= 2
                        or current_word in __ALLOWED_SINGLE_LETTER_WORDS
                    )
                ):
                    words = sorted(state.words + [current_word])
                    if len(remaining_letters) == 0:
                        visit_key = (tuple(words), tuple(sorted(remaining_letters)))
                        if visit_key not in states_visited:
                            states_visited.add(visit_key)
                            result = (words, state.words_score + child.value)
                            bisect.insort(results, result, key=lambda t: -t[1])
                            if top_n is not None:
                                results = results[:top_n]
                    else:
                        new_state = State(
                            words,
                            state.words_score + child.value,
                            "",
                            remaining_letters,
                            ws.trie(),
                        )
                        bisect.insort(
                            states,
                            new_state,
                            key=lambda s: s.current_score(),
                        )
                assert child.max_descendant_value is not None
                if (
                    minimum_word_score is None
                    or child.max_descendant_value >= minimum_word_score
                ):
                    new_state = State(
                        state.words,
                        state.words_score,
                        current_word,
                        remaining_letters,
                        child,
                    )
                    bisect.insort(
                        states,
                        new_state,
                        key=lambda s: s.current_score(),
                    )
        if len(states) > state_size_limit:
            states = states[:state_size_limit]
    return results
