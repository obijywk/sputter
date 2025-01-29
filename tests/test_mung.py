"""Tests for the mung module."""

import unittest

from sputter import mung


class MungTestCase(unittest.TestCase):
    """Tests for the mung module."""

    def test_uppercase_only(self):
        """Test the uppercase_only function."""
        self.assertEqual(mung.uppercase_only(""), "")
        self.assertEqual(mung.uppercase_only("Hello World!"), "HELLOWORLD")

    def test_uppercase_and_spaces_only(self):
        """Test the uppercase_and_spaces_only function."""
        self.assertEqual(mung.uppercase_and_spaces_only(""), "")
        self.assertEqual(mung.uppercase_and_spaces_only("Hello World!"), "HELLO WORLD")
        self.assertEqual(mung.uppercase_and_spaces_only("Hello  World!"), "HELLO WORLD")

    def test_randomly_swap_letters(self):
        """Test the random letter swapping function."""
        s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.assertEqual(len(s), 26)
        self.assertEqual(len(set(s)), 26)

        swapped_s = mung.randomly_swap_letters(s)
        self.assertEqual(len(swapped_s), 26)
        self.assertEqual(len(set(swapped_s)), 26)
        self.assertNotEqual(s, swapped_s)
        self.assertEqual(sorted(list(swapped_s)), sorted(list(s)))
