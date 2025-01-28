"""A module for determining the statistical likelihood of text being in a language."""

import gzip
import importlib.resources
import math
from typing import Optional


class QuadgramStatistics:
    """Determine text language likelihood based on quadgram frequency."""

    def __init__(self, filepath: Optional[str] = None):
        if filepath:
            with open(filepath, encoding="utf-8") as f:
                lines = f.readlines()
        else:
            data_file = importlib.resources.files("sputter.data").joinpath(
                "english_quadgrams.txt.gz"
            )
            lines = gzip.decompress(data_file.read_bytes()).decode("utf-8").split("\n")
        quadgram_freq = {}
        total = 0
        for line in lines:
            if line:
                quadgram, freq = line.split()
                int_freq = int(freq)
                quadgram_freq[quadgram] = int_freq
                total += int_freq
        self._floor = math.log(0.01 / total)
        self._quadgram_log_prob = {
            quadgram: math.log(freq / total) for quadgram, freq in quadgram_freq.items()
        }

    def quadgram_log_prob(self, quadgram: str) -> float:
        """Return the log probability of the quadgram.

        If the quadgram is not in the dictionary, return the floor value.

        :param quadgram: The quadgram to get the log probability of.
            Must be exactly 4 characters long, all uppercase.

        :return: The log probability of the quadgram.
        """
        return self._quadgram_log_prob.get(quadgram, self._floor)

    def string_score(self, s: str) -> float:
        """Return the log probability score of the string s.

        Larger scores indicate higher likelihood of the string being in the language.

        :param s: The string to score. Must only contain uppercase letters.

        :return: The log probability score of the string s.
        """
        score = 0.0
        for i in range(len(s) - 3):
            score += self.quadgram_log_prob(s[i : i + 4])
        return score


class WordStatistics:
    """Determine text language likelihood based on word frequency."""

    def __init__(self, filepath: Optional[str] = None):
        if filepath:
            with open(filepath, encoding="utf-8") as f:
                lines = f.readlines()
        else:
            data_file = importlib.resources.files("sputter.data").joinpath(
                "english_words_50k.txt.gz"
            )
            lines = gzip.decompress(data_file.read_bytes()).decode("utf-8").split("\n")
        word_freq = {}
        total = 0
        word_lengths_total = 0
        for line in lines:
            if line:
                word, freq = line.split()
                int_freq = int(freq)
                word_freq[word] = int_freq
                total += int_freq
                word_lengths_total += int_freq * len(word)
        self._floor = math.log(0.01 / total)
        self._word_log_prob = {
            word: math.log(freq / total) for word, freq in word_freq.items()
        }
        self._average_word_length = word_lengths_total / total

    def word_log_prob(
        self, word: str, scale_floor_to_word_length: bool = False
    ) -> float:
        """Return the log probability of the word.

        If the word is not in the dictionary, return the floor value.

        :param word: The word to get the log probability of.
            Must be all uppercase.
        :param scale_floor_to_word_length: If True, scale the floor value based on the
            length of the word.

        :return: The log probability of the word.
        """
        if scale_floor_to_word_length:
            floor = self._floor * len(word) / self._average_word_length
        else:
            floor = self._floor
        return self._word_log_prob.get(word, floor)

    def spaced_string_score(self, s: str) -> float:
        """Return the log probability score of the string s.

        s must contain spaces between words.

        Larger scores indicate higher likelihood of the string being in the language.

        :param s: The string to score. Must only contain uppercase letters and spaces.

        :return: The log probability score of the string s.
        """
        score = 0.0
        for word in s.split(" "):
            if not word:
                continue
            score += self.word_log_prob(word)
        return score
