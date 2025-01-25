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
            data_file = importlib.resources.files("texput.data").joinpath(
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
