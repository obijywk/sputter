"""Tests for the alphabet_trie module."""

import unittest

from sputter import alphabet_trie


class AlphabetTrieTestCase(unittest.TestCase):
    """Tests for the alphabet_trie module."""

    def test_alphabet_trie(self):
        """Tests the AlphabetTrieNode class."""
        root = alphabet_trie.AlphabetTrieNode()
        assert root.subtrie("ONE") is None

        root.insert("ONE", 1.0)
        assert root.subtrie("ONE").value == 1.0
        assert root.subtrie("ONE").min_descendant_value == 1.0

        node = root.subtrie("O")
        assert isinstance(node, alphabet_trie.AlphabetTrieNode)
        assert node.value is None
        assert node.min_descendant_value == 1.0
        assert node.subtrie("NE").value == 1.0

        node = node.subtrie("N")
        assert isinstance(node, alphabet_trie.AlphabetTrieNode)
        assert node.value is None
        assert node.min_descendant_value == 1.0
        assert node.subtrie("E").value == 1.0

        root.insert("TWO", 2.0)
        root.insert("THREE", 3.0)

        node = root.subtrie("T")
        assert node.value is None
        assert node.min_descendant_value == 2.0
        assert node.subtrie("ONE") is None
        assert node.subtrie("NE") is None
        assert node.subtrie("W").min_descendant_value == 2.0
        assert node.subtrie("WO").value == 2.0
        assert node.subtrie("H").min_descendant_value == 3.0
        assert node.subtrie("HREE").value == 3.0
