"""Tests for the spacer module."""

import pytest
import unittest

from sputter import fitness
from sputter import spacer


class SpacerTestCase(unittest.TestCase):
    """Tests for the spacer module."""

    def setUp(self):
        self.ws = fitness.WordStatistics()

    def test_space(self):
        """Tests the space function."""
        assert spacer.space("HELLOWORLD", ws=self.ws)[0][0] == "HELLO WORLD"
        assert spacer.space("HELLOXQWORLD", ws=self.ws)[0][0] == "HELLO XQ WORLD"
        assert (
            spacer.space("THISISALONGERSTRINGTOSPACE", ws=self.ws)[0][0]
            == "THIS IS A LONGER STRING TO SPACE"
        )

    def test_space_with_enumeration(self):
        """Tests the space_with_enumeration function."""
        assert spacer.space_with_enumeration("HELLOWORLD", [5, 5]) == "HELLO WORLD"
        assert (
            spacer.space_with_enumeration(
                "THISISALONGERSTRINGTOSPACE", [4, 2, 1, 6, 6, 2, 5]
            )
            == "THIS IS A LONGER STRING TO SPACE"
        )
        with pytest.raises(
            ValueError,
            match="The sum of the enumeration must equal the length of the text.",
        ):
            spacer.space_with_enumeration("HELLOWORLD", [5, 4])
