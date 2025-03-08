"""Tests for the optimize module."""

import random
import unittest

from sputter import optimize


class OptimizeTestCase(unittest.TestCase):
    """Tests for the optimize module."""

    def test_brute_force(self):
        """Tests the brute_force function."""
        assert optimize.brute_force(lambda c: -float(ord(c)), ["A", "B", "C"], 2) == [
            ("C", -67.0),
            ("B", -66.0),
        ]

    def test_simulated_annealing(self):
        """Tests the simulated_annealing function."""
        results = optimize.simulated_annealing(
            lambda c: float(abs(ord("M") - ord(c))),
            "A",
            lambda c: chr(
                max(ord("A"), min(ord("Z"), ord(c) + random.choice([-1, 1])))
            ),
            config=optimize.SimulatedAnnealingConfig(
                iterations_per_temp=10,
                initial_temp=10.0,
                min_temp=1.0,
            ),
        )
        assert len(results) == 10
        assert results[0][0] == "M"
        assert results[0][1] == 0.0
