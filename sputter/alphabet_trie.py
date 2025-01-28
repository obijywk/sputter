"""A trie where each node represents a letter of the alphabet."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class AlphabetTrieNode:
    """A node in a trie where each node represents a letter of the alphabet."""

    value: Optional[float] = None
    min_descendant_value: Optional[float] = None
    children: List[Optional["AlphabetTrieNode"]] = field(
        default_factory=lambda: [None] * 26
    )

    __ORD_A = ord("A")

    def subtrie(self, word: str) -> Optional["AlphabetTrieNode"]:
        """Return the subtrie starting with the given word."""
        if not word:
            return self
        child = self.children[ord(word[0]) - self.__ORD_A]
        if child:
            return child.subtrie(word[1:])
        return None

    def insert(self, word: str, value: float):
        """Insert a word into the trie."""
        if self.min_descendant_value is None or value < self.min_descendant_value:
            self.min_descendant_value = value
        if not word:
            self.value = value
            return
        child = self.children[ord(word[0]) - self.__ORD_A]
        if not child:
            child = AlphabetTrieNode()
            self.children[ord(word[0]) - self.__ORD_A] = child
        child.insert(word[1:], value)
