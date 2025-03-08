"""A module for separating multiple interspersed words."""

from dataclasses import dataclass
from typing import List, Optional, Tuple

from sputter.alphabet_trie import AlphabetTrieNode
from sputter.fitness import WordStatistics


@dataclass
class Config:
    """Configuration for unweaver."""

    min_words: Optional[int] = None
    """The minimum number of words allowed in the output."""

    max_words: Optional[int] = None
    """The maximum number of words allowed in the output."""

    state_size_limit: int = 8192
    """The maximum number of states to keep in memory at any given time."""

    ws: Optional[WordStatistics] = None
    """A WordStatistics object. If None, one will be constructed."""


def unweave(
    s: str,
    top_n: Optional[int] = 10,
    config: Optional[Config] = None,
) -> List[Tuple[List[str], float]]:
    """Separate a string containing multiple interspersed words into separate words.

    :param s: The interspersed text. Must only contain uppercase letters.
    :param top_n: The number of results to return.
    :param config: Configuration for the unweaver. If None, default values will be used.

    :return: A list of tuples, where each tuple contains a list of words and its score.
    """
    if config is None:
        config = Config()
    ws = config.ws
    if ws is None:
        ws = WordStatistics()
    trie = ws.trie()
    max_words = config.max_words

    @dataclass
    class State:
        """A state in the search."""

        score: float
        trie_nodes: List[AlphabetTrieNode]
        words: List[str]

        def __lt__(self, other: "State") -> bool:
            return self.score < other.score

        def advance(self, c: str) -> List["State"]:
            """Return the set of states that may be created by adding a character."""
            new_states = []
            for i, (node, word) in enumerate(
                zip(self.trie_nodes, self.words, strict=True)
            ):
                new_node = node.subtrie(c)
                if new_node is not None:
                    node_score = node.value or node.min_descendant_value
                    new_node_score = new_node.value or new_node.min_descendant_value
                    assert node_score is not None
                    assert new_node_score is not None
                    new_nodes = (
                        self.trie_nodes[:i] + [new_node] + self.trie_nodes[i + 1 :]
                    )
                    new_words = self.words[:i] + [word + c] + self.words[i + 1 :]
                    new_score = self.score + node_score - new_node_score
                    new_states.append(State(new_score, new_nodes, new_words))
            if not max_words or len(self.trie_nodes) < max_words:
                new_node = trie.subtrie(c)
                if new_node is not None:
                    new_node_score = new_node.value or new_node.min_descendant_value
                    assert new_node_score is not None
                    new_score = self.score - new_node_score
                    new_states.append(
                        State(
                            new_score,
                            self.trie_nodes + [new_node],
                            self.words + [c],
                        )
                    )
            return new_states

        def is_complete(self) -> bool:
            """Return True if this state is complete."""
            return all(node.value is not None for node in self.trie_nodes)

    states: List[State] = [State(0.0, [], [])]
    for c in s:
        new_states: List[State] = []
        word_sets = set()
        for state in states:
            for new_state in state.advance(c):
                word_set = tuple(sorted(new_state.words))
                if word_set not in word_sets:
                    word_sets.add(word_set)
                    new_states.append(new_state)
        states = sorted(new_states)[: config.state_size_limit]
    states = [
        state
        for state in states
        if state.is_complete()
        and (not config.min_words or len(state.words) >= config.min_words)
    ]
    if top_n:
        states = states[:top_n]
    return [(state.words, state.score) for state in states]
