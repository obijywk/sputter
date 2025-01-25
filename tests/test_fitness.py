"""Tests for the fitness module."""

import unittest

from texput import fitness


class QuadgramStatisticsTestCase(unittest.TestCase):
    """Tests for the QuadgramStatistics class."""

    def setUp(self):
        self.qs = fitness.QuadgramStatistics()

    def test_quadgram_log_prob(self):
        """Test that quadgram log probabilities are computed correctly."""
        self.assertGreater(
            self.qs.quadgram_log_prob("THIS"), self.qs.quadgram_log_prob("QXZJ")
        )

    def test_string_score(self):
        """Test that the score of a common string is greater than that of a rare one."""
        self.assertGreater(
            self.qs.string_score("THISISATEST"), self.qs.string_score("QXZJVJIAOLOX")
        )
