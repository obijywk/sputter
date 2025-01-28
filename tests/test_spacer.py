"""Tests for the spacer module."""

import unittest

from sputter import spacer


class SpacerTestCase(unittest.TestCase):
    """Tests for the spacer module."""

    def test_space(self):
        """Tests the space function."""
        self.assertEqual(spacer.space("HELLOWORLD")[0][0], "HELLO WORLD")
        self.assertEqual(spacer.space("HELLOXQWORLD")[0][0], "HELLO XQ WORLD")
