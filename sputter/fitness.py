"""A module for determining the statistical likelihood of text being in a language."""

import gzip
import importlib.resources
import math
import re
from typing import Dict, Optional

from sputter.alphabet_trie import AlphabetTrieNode


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

        :return: The log probability of the quadgram. Returned values are in the range
            of negative infinity to zero, where negative infinity is the least likely
            probability and zero is the most likely probability.
        """
        return self._quadgram_log_prob.get(quadgram, self._floor)

    def string_score(self, s: str) -> float:
        """Return the log probability score of the string s.

        Greater scores indicate higher likelihood of the string being in the language.

        :param s: The string to score. Must be at least four characters long and
            only contain uppercase letters.

        :return: The log probability score of the string s. Returned values are in the
            range of negative infinity to zero, where negative infinity is the least
            likely probability and zero is the most likely probability.
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
        non_letter_re = re.compile(r"[^A-Z]")
        self._word_freq: Dict[str, int] = {}
        self._word_freq_total = 0
        word_lengths_total = 0
        for line in lines:
            if line:
                word, freq = line.split()
                if not word:
                    continue
                word = word.upper()
                if re.search(non_letter_re, word):
                    continue
                int_freq = int(freq)
                self._word_freq[word] = int_freq
                self._word_freq_total += int_freq
                word_lengths_total += int_freq * len(word)
        self._floor = math.log(0.01 / self._word_freq_total)
        self._word_log_prob = {
            word: math.log(freq / self._word_freq_total)
            for word, freq in self._word_freq.items()
        }
        self._average_word_length = word_lengths_total / self._word_freq_total
        self._trie: Optional[AlphabetTrieNode] = None

    def word_frequencies(self) -> Dict[str, int]:
        """Return a dictionary from word to number of occurrences of that word."""
        return self._word_freq

    def word_frequency_total(self) -> int:
        """Return the total number of occurrences of all words."""
        return self._word_freq_total

    def word_log_prob(
        self, word: str, scale_floor_to_word_length: bool = False
    ) -> float:
        """Return the log probability of the word.

        If the word is not in the dictionary, return the floor value.

        :param word: The word to get the log probability of. Must be all uppercase.
        :param scale_floor_to_word_length: If True, scale the floor value based on the
            length of the word.

        :return: The log probability of the word. Returned values are in the range
            of negative infinity to zero, where negative infinity is the least likely
            probability and zero is the most likely probability.
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

        :return: The log probability score of the string s. Returned values are in the
            range of negative infinity to zero, where negative infinity is the least
            likely probability and zero is the most likely probability.
        """
        score = 0.0
        for word in s.split(" "):
            if not word:
                continue
            score += self.word_log_prob(word)
        return score

    def trie(self) -> AlphabetTrieNode:
        """Return a trie of all words containing their log probabilities."""
        if not self._trie:
            self._trie = AlphabetTrieNode()
            for word, log_prob in self._word_log_prob.items():
                self._trie.insert(word, log_prob)
        return self._trie
