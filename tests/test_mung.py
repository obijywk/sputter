"""Tests for the mung module."""

import unittest

from texput import mung


class MungTestCase(unittest.TestCase):
    """Tests for the mung module."""

    def test_uppercase_only(self):
        """Test the uppercase_only function."""
        self.assertEqual(mung.uppercase_only(""), "")
        self.assertEqual(mung.uppercase_only("Hello World!"), "HELLOWORLD")
