"""Tests for the alphabet_trie module."""

import unittest

from sputter import alphabet_trie


class AlphabetTrieTestCase(unittest.TestCase):
    """Tests for the alphabet_trie module."""

    def test_alphabet_trie(self):
        """Tests the AlphabetTrieNode class."""
        root = alphabet_trie.AlphabetTrieNode()
        self.assertIsNone(root.subtrie("ONE"))

        root.insert("ONE", 1.0)
        self.assertEqual(root.subtrie("ONE").value, 1.0)
        self.assertEqual(root.subtrie("ONE").min_descendant_value, 1.0)

        node = root.subtrie("O")
        self.assertIsInstance(node, alphabet_trie.AlphabetTrieNode)
        self.assertIsNone(node.value)
        self.assertEqual(node.min_descendant_value, 1.0)
        self.assertEqual(node.subtrie("NE").value, 1.0)

        node = node.subtrie("N")
        self.assertIsInstance(node, alphabet_trie.AlphabetTrieNode)
        self.assertIsNone(node.value)
        self.assertEqual(node.min_descendant_value, 1.0)
        self.assertEqual(node.subtrie("E").value, 1.0)

        root.insert("TWO", 2.0)
        root.insert("THREE", 3.0)

        node = root.subtrie("T")
        self.assertIsNone(node.value)
        self.assertEqual(node.min_descendant_value, 2.0)
        self.assertIsNone(node.subtrie("ONE"))
        self.assertIsNone(node.subtrie("NE"))
        self.assertEqual(node.subtrie("W").min_descendant_value, 2.0)
        self.assertEqual(node.subtrie("WO").value, 2.0)
        self.assertEqual(node.subtrie("H").min_descendant_value, 3.0)
        self.assertEqual(node.subtrie("HREE").value, 3.0)
