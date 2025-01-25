"""Tests for the optimize module."""

import unittest

from texput import optimize


class OptimizeTestCase(unittest.TestCase):
    """Tests for the optimize module."""

    def test_brute_force(self):
        """Tests the brute_force function."""
        self.assertEqual(
            optimize.brute_force(lambda c: float(ord(c)), ["A", "B", "C"], 2),
            [("C", 67.0), ("B", 66.0)],
        )
