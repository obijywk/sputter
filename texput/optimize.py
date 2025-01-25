"""A module to search for optimal inputs with respect to objectives."""

import bisect
from typing import Callable, Iterable, List, Optional, Tuple, TypeVar


T = TypeVar("T")


def brute_force(
    objective_function: Callable[[T], float],
    search_space: Iterable[T],
    top_n: Optional[int] = 10,
) -> List[Tuple[T, float]]:
    """Search for optimal inputs for the objective function by testing every input.

    :param objective_function: A Callable that takes a T as input and returns a
        score. Higher scores are better.
    :param search_space: An iterable of T to test as inputs to the function.
    :param top_n: The number of top results to return. If None, return all results.

    :return: A list of tuples, where each tuple contains a string from the search space
        and its corresponding score.
    """
    results: List[Tuple[T, float]] = []
    for s in search_space:
        score = objective_function(s)
        if not results or score > results[-1][1]:
            bisect.insort(results, (s, score), key=lambda t: -t[1])
            results = results[:top_n]
    return results
