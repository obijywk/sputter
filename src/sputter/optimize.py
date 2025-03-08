"""A module to search for optimal inputs with respect to objectives."""

import bisect
from dataclasses import dataclass
import math
import random
from typing import Callable, Iterable, List, Optional, Tuple, TypeVar


T = TypeVar("T")


def brute_force(
    objective_function: Callable[[T], float],
    search_space: Iterable[T],
    top_n: Optional[int] = 10,
) -> List[Tuple[T, float]]:
    """Search for optimal inputs for the objective function by testing every input.

    :param objective_function: A Callable that takes a T as input and returns a
        score. Lower scores are better.
    :param search_space: An iterable of T to test as inputs to the function.
    :param top_n: The number of top results to return. If None, return all results.

    :return: A list of tuples, where each tuple contains a string from the search space
        and its corresponding score.
    """
    results: List[Tuple[T, float]] = []
    for s in search_space:
        score = objective_function(s)
        if not results or score < results[-1][1]:
            bisect.insort(results, (s, score), key=lambda t: t[1])
            if top_n is not None:
                results = results[:top_n]
    return results


@dataclass
class SimulatedAnnealingConfig[T]:
    """Configuration for simulated annealing."""

    alpha: float = 0.9
    """The alpha parameter determines the annealing schedule. At each temperature
    change, the temperature is set to the current temperature multiplied by alpha."""

    iterations_per_temp: int = 10000
    """The number of iterations to perform at each temperature."""

    initial_temp: float = 10000.0
    """The initial temperature. The search will start at this temperature."""

    min_temp: float = 0.1
    """The minimum temperature. The search will stop when the temperature reaches this
    value."""

    progress_callback: Optional[Callable[[float, T, float], None]] = None
    """A callback that is called after each temperature change.

    It is passed the current temperature, the best state found so far, and the best
    state score found so far."""


def simulated_annealing(
    objective_function: Callable[[T], float],
    initial_state: T,
    neighbor_function: Callable[[T], T],
    top_n: Optional[int] = 10,
    config: Optional[SimulatedAnnealingConfig] = None,
) -> List[Tuple[T, float]]:
    """Search for optimal inputs for the objective using simulated annealing.

    :param objective_function: A Callable that takes a T as input and returns a
        score. Lower scores are better.
    :param initial_state: The initial state to start the search from. This is
        typically a random state.
    :param neighbor_function: A Callable that takes a T as input and returns a
        neighboring state. This is typically a small random change to the input.
    :param top_n: The number of top results to return. If None, all results are
        returned.
    :param config: The configuration for the simulated annealing algorithm.

    :return: A list of tuples of the form (state, score), sorted by score in
        ascending order. The list is truncated to the top_n results if top_n is not
        None.
    """
    if config is None:
        config = SimulatedAnnealingConfig()
    temperature = config.initial_temp
    state = initial_state
    state_score = objective_function(state)
    i = 0
    results: List[Tuple[T, float]] = []
    while temperature > config.min_temp:
        neighbor_state = neighbor_function(state)
        neighbor_score = objective_function(neighbor_state)
        delta_score = neighbor_score - state_score
        if delta_score < 0:
            acceptance_probability = 1.0
        else:
            acceptance_probability = math.exp(-delta_score / temperature)
        if acceptance_probability > random.random():
            state = neighbor_state
            state_score = neighbor_score
            if not results or state_score < results[-1][1]:
                result_index = bisect.bisect_left(
                    results, state_score, key=lambda t: t[1]
                )
                if not results or results[result_index][0] != state:
                    results.insert(result_index, (state, state_score))
                    if top_n is not None and len(results) > top_n:
                        results = results[:top_n]
        i += 1
        if i >= config.iterations_per_temp:
            temperature *= config.alpha
            i = 0
            if config.progress_callback:
                config.progress_callback(temperature, results[0][0], results[0][1])
    return results
