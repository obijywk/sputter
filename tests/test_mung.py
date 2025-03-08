"""Tests for the mung module."""

import unittest

from sputter import mung


class MungTestCase(unittest.TestCase):
    """Tests for the mung module."""

    def test_uppercase_only(self):
        """Test the uppercase_only function."""
        assert mung.uppercase_only("") == ""
        assert mung.uppercase_only("Hello World!") == "HELLOWORLD"

    def test_uppercase_and_spaces_only(self):
        """Test the uppercase_and_spaces_only function."""
        assert mung.uppercase_and_spaces_only("") == ""
        assert mung.uppercase_and_spaces_only("Hello World!") == "HELLO WORLD"
        assert mung.uppercase_and_spaces_only("Hello  World!") == "HELLO WORLD"

    def test_randomly_swap_letters(self):
        """Test the random letter swapping function."""
        s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        assert len(s) == 26
        assert len(set(s)) == 26

        swapped_s = mung.randomly_swap_letters(s)
        assert len(swapped_s) == 26
        assert len(set(swapped_s)) == 26
        assert s != swapped_s
        assert sorted(swapped_s) == sorted(s)
