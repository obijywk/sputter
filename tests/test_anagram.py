"""Tests for the anagram module."""

import unittest

from sputter.anagram import anagram_phrase
from sputter.fitness import WordStatistics


class AnagramTestCase(unittest.TestCase):
    """Tests for the anagram module."""

    def test_anagram_phrase(self):
        """Test the anagram phrase function."""
        ws = WordStatistics()
        assert anagram_phrase("", ws) == []

        results = anagram_phrase("EHLLO", ws, max_words=1)
        assert len(results) == 1
        assert results[0][0][0][0] == "HELLO"

        results = anagram_phrase("OPST", ws, max_words=1)
        assert len(results) == 1
        words = set(results[0][0][0])
        assert "POST" in words
        assert "POTS" in words
        assert "SPOT" in words
        assert "STOP" in words
        assert "TOPS" in words

        results = anagram_phrase("ABEEHILMNSSTT", ws, max_words=1)
        assert len(results) == 1
        assert results[0][0][0][0] == "ESTABLISHMENT"

        results = anagram_phrase("DEHLLLOORW", ws, min_words=2, max_words=2)
        words = {w[0] for w in results[0][0]}
        assert len(words) == 2
        assert "HELLO" in words
        assert "WORLD" in words

        results = anagram_phrase("AAACCCJJJKKK", ws, min_words=3, max_words=3)
        assert len(results) == 1
        assert len(results[0][0]) == 3
        for word_list in results[0][0]:
            assert word_list == ["JACK"]
