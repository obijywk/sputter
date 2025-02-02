"""Example program to evaluate word features."""

import cProfile
import pstats
import time
from typing import List

from sputter.word_features import WordFeatureResult, WordFeatureStatistics


def print_results(results: List[WordFeatureResult]):
    """Print the results of evaluating word features."""
    for result in results:
        print(f"{result.log_prob:10.2f} {result.feature} {result.words}")


def main(enable_profiling: bool = False):
    """Example program to evaluate word features."""

    if enable_profiling:
        profile = cProfile.Profile()
        start_time = time.time()
        profile.enable()
    wfs = WordFeatureStatistics()
    if enable_profiling:
        profile.disable()
        end_time = time.time()
        print(
            f"Initialized WordFeatureStatistics in {end_time - start_time:.2f} seconds"
        )
        pstats.Stats(profile).sort_stats("cumtime").print_stats(30)

    words = [
        "STEPSISTERS",
        "ERNIEELS",
        "SINNFEIN",
        "NINEONEONE",
        "SUSPENDEDSENTENCE",
    ]
    print(words)
    print_results(wfs.evaluate_words(words))
    print()

    words = [
        "LOLL",
        "SANAA",
        "OBSESS",
        "PRETEEN",
        "FIREWEED",
        "DODDFRANK",
    ]
    print(words)
    print_results(wfs.evaluate_words(words))
    print()

    words = [
        "CROC",
        "CONE",
        "NIOBE",
        "NOES",
        "BOY",
        "COOK",
        "BHOPA",
        "KONA",
        "CROW",
    ]
    print(words)
    print_results(wfs.evaluate_words(words))
    print()


if __name__ == "__main__":
    main(enable_profiling=False)
