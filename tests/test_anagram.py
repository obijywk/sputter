"""Tests for the anagram module."""

import unittest

from sputter.anagram import anagram_phrase, anagram_word
from sputter.fitness import WordStatistics


class AnagramTestCase(unittest.TestCase):
    """Tests for the anagram module."""

    def test_anagram_word(self):
        """Test the anagram word function."""
        ws = WordStatistics()
        assert anagram_word("", ws) == []

        results = anagram_word("EHLLO", ws)
        assert len(results) == 1
        assert results[0][0] == "HELLO"

        results = anagram_word("OPST", ws)
        words = {r[0] for r in results}
        assert "POST" in words
        assert "POTS" in words
        assert "SPOT" in words
        assert "STOP" in words
        assert "TOPS" in words

        results = anagram_word("ABEEHILMNSSTT", ws)
        assert len(results) == 1
        assert results[0][0] == "ESTABLISHMENT"

    def test_anagram_phrase(self):
        """Test the anagram phrase function."""
        ws = WordStatistics()
        assert anagram_phrase("", ws=ws) == []

        results = anagram_phrase("DEHLLLOORW", ws=ws)
        assert results[0][0] == ["HELLO", "WORLD"]
