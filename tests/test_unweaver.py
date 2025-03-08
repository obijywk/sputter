"""Tests for the unweaver module."""

import unittest

from sputter import fitness
from sputter import unweaver


class UnweaverTestCase(unittest.TestCase):
    """Tests for the unweaver module."""

    def setUp(self):
        self.ws = fitness.WordStatistics()
        self.trie = self.ws.trie()

    def test_unweave(self):
        """Tests the unweave function."""
        assert unweaver.unweave("TEST", config=unweaver.Config(ws=self.ws))[0][0] == [
            "TEST"
        ]
        assert unweaver.unweave("TOENSET", config=unweaver.Config(ws=self.ws))[0][
            0
        ] == ["TEST", "ONE"]
        assert unweaver.unweave(
            "RCAHSEPEBESRERCYAKE",
            config=unweaver.Config(min_words=3, max_words=3, ws=self.ws),
        )[0][0] == ["RASPBERRY", "CHEESE", "CAKE"]
        assert unweaver.unweave(
            "TFMTHUREUOSDRISNDDDAAAYAYYY",
            config=unweaver.Config(max_words=4, ws=self.ws),
        )[0][0] == ["THURSDAY", "FRIDAY", "MONDAY", "TUESDAY"]
        assert unweaver.unweave(
            "AINNATERSRCTATHENYIDENOETDORYALONCALTBLRANYD",
            config=unweaver.Config(max_words=6, ws=self.ws),
        )[0][0] == ["ANARCHY", "INTERSTATE", "NINETY", "DEODORANT", "LOCALLY", "BRAND"]
