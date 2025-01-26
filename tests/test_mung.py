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
