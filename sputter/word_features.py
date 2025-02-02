"""A module for detecting interesting features of words.

Inspired by https://github.com/rdeits/Collective.jl.
"""

# pylint: disable=too-few-public-methods

from collections import defaultdict
from dataclasses import dataclass
import math
from typing import Dict, List, Optional

from sputter.fitness import WordStatistics


ALPHABET = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
VOWELS = set("AEIOU")
CONSONANTS = ALPHABET - VOWELS


class WordFeature:
    """A base class for detecting an interesting feature of a word."""

    def evaluate(self, word: str) -> bool:
        """Return true iff the word has this feature."""
        raise NotImplementedError


@dataclass(frozen=True)
class LetterCountFeature(WordFeature):
    """Word features based on number of letter occurrences."""

    letter: str
    """The letter to count. Must be uppercase."""

    min_count: int
    """The minimum number of occurrences of the letter to satisfy this feature."""

    def evaluate(self, word: str) -> bool:
        return word.count(self.letter) >= self.min_count

    def __repr__(self) -> str:
        return f"contains at least {self.min_count} occurrences of {self.letter}"


@dataclass(frozen=True)
class UniqueLetterCountFeature(WordFeature):
    """Word features based on number of unique letter occurrences."""

    count: int
    """The number of unique letters to satisfy this feature."""

    def evaluate(self, word: str) -> bool:
        return len(set(word)) == self.count

    def __repr__(self) -> str:
        return f"contains {self.count} unique letters"


@dataclass(frozen=True)
class UniqueVowelCountFeature(WordFeature):
    """Word features based on number of unique vowel occurrences."""

    count: int
    """The number of unique vowels to satisfy this feature."""

    def evaluate(self, word: str) -> bool:
        return len(set(word) & VOWELS) == self.count

    def __repr__(self) -> str:
        return f"contains {self.count} unique vowels"


@dataclass(frozen=True)
class UniqueConsonantCountFeature(WordFeature):
    """Word features based on number of unique consonant occurrences."""

    count: int
    """The number of unique consonants to satisfy this feature."""

    def evaluate(self, word: str) -> bool:
        return len(set(word) & CONSONANTS) == self.count

    def __repr__(self) -> str:
        return f"contains {self.count} unique consonants"


@dataclass(frozen=True)
class AlternatesVowelConsonantFeature(WordFeature):
    """Word features based on alternating vowel and consonant occurrences."""

    def evaluate(self, word: str) -> bool:
        last_was_vowel = word[0] in VOWELS
        for c in word[1:]:
            if c in VOWELS:
                if last_was_vowel:
                    return False
            elif not last_was_vowel:
                return False
            last_was_vowel = c in VOWELS
        return True

    def __repr__(self) -> str:
        return "alternates between vowels and consonants"


@dataclass(frozen=True)
class DoubleLettersFeature(WordFeature):
    """Word features based on number of occurrences of double letters."""

    count: int
    """The number of double letters to satisfy this feature."""

    def evaluate(self, word: str) -> bool:
        return (
            sum(1 for i in range(len(word) - 1) if word[i] == word[i + 1]) == self.count
        )

    def __repr__(self) -> str:
        return f"contains {self.count} pairs of double letters"


ALL_FEATURES: List[WordFeature] = [
    AlternatesVowelConsonantFeature(),
]
ALL_FEATURES.extend(
    [LetterCountFeature(letter, count) for letter in ALPHABET for count in range(1, 5)]
)
ALL_FEATURES.extend([UniqueLetterCountFeature(count) for count in range(1, 27)])
ALL_FEATURES.extend(
    [UniqueVowelCountFeature(count) for count in range(1, len(VOWELS) + 1)]
)
ALL_FEATURES.extend(
    [UniqueConsonantCountFeature(count) for count in range(1, len(CONSONANTS) + 1)]
)
ALL_FEATURES.extend([DoubleLettersFeature(count) for count in range(1, 4)])


@dataclass
class WordFeatureResult:
    """The result of evaluating a word feature on a set of words."""

    feature: WordFeature
    """The word feature that was evaluated."""

    log_prob: float
    """The log probability of the feature evaluating true for the set of words."""


class WordFeatureStatistics:
    """A class for computing statistics about word features."""

    def __init__(self, ws: Optional[WordStatistics] = None):
        """Initialize a set of word feature statistics based on word frequencies.

        :param ws: The WordStatistics to use. If None, a new WordStatistics will be
            created.
        """
        self._ws = ws or WordStatistics()

        self._feature_count: Dict[WordFeature, int] = defaultdict(int)

        for word, freq in self._ws.word_frequencies().items():
            for feature in ALL_FEATURES:
                if feature.evaluate(word):
                    self._feature_count[feature] += freq

        word_frequency_total = self._ws.word_frequency_total()
        self._feature_log_prob = {
            feature: math.log(count / word_frequency_total)
            for feature, count in self._feature_count.items()
        }

    def evaluate_words(
        self, words: List[str], top_n: Optional[int] = 10
    ) -> List[WordFeatureResult]:
        """Evaluate a set of words against all word features.

        :param words: The words to evaluate.
        :param top_n: The number of top results to return. If None, all results will be
            returned.

        :return: A list of WordFeatureResults, one for each word feature. The list is
            sorted by log probability, from least likely to most likely.
        """
        results = []
        for feature, feature_log_prob in self._feature_log_prob.items():
            if all(feature.evaluate(word) for word in words):
                results.append(
                    WordFeatureResult(feature, feature_log_prob * len(words))
                )
        results.sort(key=lambda result: result.log_prob)
        if top_n is not None:
            results = results[:top_n]
        return results
