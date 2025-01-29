"""Tests for the spacer module."""

import unittest

from sputter import fitness
from sputter import spacer


class SpacerTestCase(unittest.TestCase):
    """Tests for the spacer module."""

    def setUp(self):
        self.ws = fitness.WordStatistics()

    def test_space(self):
        """Tests the space function."""
        self.assertEqual(spacer.space("HELLOWORLD", ws=self.ws)[0][0], "HELLO WORLD")
        self.assertEqual(
            spacer.space("HELLOXQWORLD", ws=self.ws)[0][0], "HELLO XQ WORLD"
        )
        self.assertEqual(
            spacer.space("THISISALONGERSTRINGTOSPACE", ws=self.ws)[0][0],
            "THIS IS A LONGER STRING TO SPACE",
        )
