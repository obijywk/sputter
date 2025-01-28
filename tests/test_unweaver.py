"""Tests for the unweaver module."""

import unittest

from sputter import unweaver


class UnweaverTestCase(unittest.TestCase):
    """Tests for the unweaver module."""

    def test_unweave(self):
        """Tests the unweave function."""
        self.assertEqual(unweaver.unweave("TEST")[0][0], ["TEST"])
        self.assertEqual(unweaver.unweave("TOENSET")[0][0], ["TEST", "ONE"])
        self.assertEqual(
            unweaver.unweave(
                "RCAHSEPEBESRERCYAKE", config=unweaver.Config(min_words=3, max_words=3)
            )[0][0],
            ["RASPBERRY", "CHEESE", "CAKE"],
        )
        self.assertEqual(
            unweaver.unweave(
                "TFMTHUREUOSDRISNDDDAAAYAYYY", config=unweaver.Config(max_words=4)
            )[0][0],
            ["THURSDAY", "FRIDAY", "MONDAY", "TUESDAY"],
        )
        self.assertEqual(
            unweaver.unweave(
                "AINNATERSRCTATHENYIDENOETDORYALONCALTBLRANYD",
                config=unweaver.Config(max_words=6),
            )[0][0],
            ["ANARCHY", "INTERSTATE", "NINETY", "DEODORANT", "LOCALLY", "BRAND"],
        )
