"""Tests for the coincidence module."""

import unittest

from sputter import coincidence


class CoincidenceTestCase(unittest.TestCase):
    """Tests for the coincidence module."""

    def test_index_of_coincidence(self):
        assert coincidence.index_of_coincidence("A") == 26.0
        assert coincidence.index_of_coincidence("AAAA") == 26.0
        assert coincidence.index_of_coincidence("ABCD") == 0.0
        assert coincidence.index_of_coincidence("AABB") == 26.0 / 3

    def test_delta_bar(self):
        assert coincidence.delta_bar("AAAA", 1) == 26.0
        assert coincidence.delta_bar("AAAA", 2) == 26.0
        assert coincidence.delta_bar("ABAB", 2) == 26.0
        assert coincidence.delta_bar("AABB", 2) == 0.0
        assert coincidence.delta_bar("ABCABCABC", 3) == 26.0
        assert coincidence.delta_bar("AAABBBCCC", 3) == 0.0
