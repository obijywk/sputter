"""Tests for the word_features module."""

import unittest

from sputter.word_features import (
    DoubleLettersFeature,
    UniqueVowelCountFeature,
    WordFeatureStatistics,
)


class TestWordFeatureStatistics(unittest.TestCase):
    """Tests for the WordFeatureStatistics class."""

    def setUp(self):
        self.wfs = WordFeatureStatistics()

    def test_evaluate_words(self):
        """Test evaluating word feature statistics for a set of words."""
        assert isinstance(
            self.wfs.evaluate_words(["BALLOON", "BARROOM"])[0].feature,
            DoubleLettersFeature,
        )
        all_vowels_results = self.wfs.evaluate_words(
            ["EDUCATION", "FACETIOUS", "SEQUOIA", "BALLOON"]
        )
        assert isinstance(all_vowels_results[0].feature, UniqueVowelCountFeature)
        assert all_vowels_results[0].feature.count == 5
        assert set(all_vowels_results[0].words) == {"EDUCATION", "FACETIOUS", "SEQUOIA"}
