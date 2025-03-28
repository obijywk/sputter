from collections import defaultdict, Counter
import math
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from typing import Callable, List, Optional, Tuple

from sputter.fitness import WordStatistics


def anagram_phrase(
    letters: str,
    ws: Optional[WordStatistics] = None,
    top_n: int = 10,
    min_words: Optional[int] = None,
    max_words: Optional[int] = None,
    result_callback: Optional[Callable[[List[List[str]], float], None]] = None,
) -> List[Tuple[List[List[str]], float]]:
    """Return phrases that can be formed from the given letters.

    :param letters: The letters to be anagrammed.
    :param ws: The WordStatistics to use. If None, a new WordStatistics will be
        created.
    :param top_n: The maximum number of results to return.
    :param min_words: The minimum number of words allowed in the output.
    :param max_words: The maximum number of words allowed in the output.
    :param result_callback: A callback function that will be called with each
        result as it is found. The callback should take two arguments: a list of words
        and their fitness score.
    """
    if not ws:
        ws = WordStatistics()
    if not letters:
        return []

    letter_counts = Counter(sorted(letters))
    letter_set = set(letter_counts.keys())

    def word_to_letter_count_vector(word: str) -> Optional[List[int]]:
        if not set(word).issubset(letter_set):
            return None
        word_letter_counts = Counter(word)
        v = []
        for c, n in letter_counts.items():
            wn = word_letter_counts[c]
            if wn > n:
                return None
            v.append(wn)
        return v

    sorted_words = []
    sorted_word_to_words = defaultdict(list)
    word_letter_count_vectors = []
    for word in ws.word_frequencies():
        if len(word) == 1 and word not in {"A", "I"}:
            continue
        sorted_word = "".join(sorted(word))
        if sorted_word in sorted_word_to_words:
            sorted_word_to_words[sorted_word].append(word)
        else:
            v = word_to_letter_count_vector(sorted_word)
            if v is not None:
                sorted_words.append(sorted_word)
                sorted_word_to_words[sorted_word].append(word)
                word_letter_count_vectors.append(v)

    word_id_costs = np.array(
        [
            min(-ws.word_log_prob(w) for w in sorted_word_to_words[sorted_word])
            for sorted_word in sorted_words
        ]
    )
    word_id_max_usages = np.array(
        [math.floor(len(letters) / len(w)) for w in sorted_words]
    )
    word_letter_counts = np.array(word_letter_count_vectors).transpose()
    total_letter_counts = np.array(word_to_letter_count_vector(letters))

    constraints = [
        LinearConstraint(word_letter_counts, total_letter_counts, total_letter_counts)
    ]
    if min_words:
        constraints.append(
            LinearConstraint(np.ones(len(sorted_words)), min_words, np.inf)
        )
    if max_words:
        constraints.append(
            LinearConstraint(np.ones(len(sorted_words)), -np.inf, max_words)
        )

    results: List[Tuple[List[List[str]], float]] = []
    while len(results) < top_n:
        result = milp(
            word_id_costs,
            integrality=np.ones(len(sorted_words), dtype=int),
            bounds=Bounds(np.zeros(len(sorted_words)), word_id_max_usages),
            constraints=constraints,
        )
        if not result.success:
            break
        word_ids = np.where(result.x > 0.5)[0]
        words = []
        for word_id in word_ids:
            n = round(result.x[word_id])
            words.extend([sorted_word_to_words[sorted_words[word_id]]] * n)
        results.append((words, result.fun))
        if result_callback:
            result_callback(results[-1][0], results[-1][1])
        for i in word_ids:
            word_id_max_usages[i] = 0
    return results
