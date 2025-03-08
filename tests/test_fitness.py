"""Tests for the fitness module."""

import unittest

from sputter import fitness


class QuadgramStatisticsTestCase(unittest.TestCase):
    """Tests for the QuadgramStatistics class."""

    def setUp(self):
        self.qs = fitness.QuadgramStatistics()

    def test_quadgram_log_prob(self):
        """Test that quadgram log probabilities are computed correctly."""
        assert self.qs.quadgram_log_prob("THIS") > self.qs.quadgram_log_prob("QXZJ")

    def test_string_score(self):
        """Test that the score of a common string is greater than that of a rare one."""
        assert self.qs.string_score("THISISATEST") > self.qs.string_score(
            "QXZJVJIAOLOX"
        )


class WordStatisticsTestCase(unittest.TestCase):
    """Tests for the WordStatistics class."""

    def setUp(self):
        self.ws = fitness.WordStatistics()

    def test_word_log_prob(self):
        """Test that word log probabilities are computed correctly."""
        assert self.ws.word_log_prob("THIS") > self.ws.word_log_prob("RARE")
        assert self.ws.word_log_prob("ZXQ") == self.ws.word_log_prob("ZXQJ")
        assert self.ws.word_log_prob("ZXQ", True) > self.ws.word_log_prob("ZXQJ", True)

    def test_spaced_string_score(self):
        """Test that the score of a common string is greater than that of a rare one."""
        assert self.ws.spaced_string_score(
            "THIS IS A TEST"
        ) > self.ws.spaced_string_score("RARE TERMS USED INTERNALLY")
        assert self.ws.spaced_string_score(
            "RARE TERMS USED INTERNALLY"
        ) > self.ws.spaced_string_score("QXJZV VJWXZ QZVJ QXJV")

    def test_trie(self):
        """Test that the trie is built correctly."""
        trie = self.ws.trie()
        assert trie == self.ws.trie()
        assert trie.subtrie("THIS").value == self.ws.word_log_prob("THIS")
        assert trie.subtrie("RARE").value == self.ws.word_log_prob("RARE")
        assert trie.subtrie("ZXQ") is None
