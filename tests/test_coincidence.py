"""Tests for the coincidence module."""

import pytest
import unittest

from sputter import coincidence
from sputter.mung import uppercase_only


class CoincidenceTestCase(unittest.TestCase):
    """Tests for the coincidence module."""

    def test_index_of_coincidence(self):
        assert coincidence.index_of_coincidence("A") == 1.0
        assert coincidence.index_of_coincidence("AAAA") == 1.0
        assert coincidence.index_of_coincidence("ABCD") == 0.0
        assert coincidence.index_of_coincidence("AABB") == 1.0 / 3

    def test_delta_bar(self):
        assert coincidence.delta_bar("AAAA", 1) == 26.0
        assert coincidence.delta_bar("AAAA", 2) == 26.0
        assert coincidence.delta_bar("ABAB", 2) == 26.0
        assert coincidence.delta_bar("AABB", 2) == 0.0
        assert coincidence.delta_bar("ABCABCABC", 3) == 26.0
        assert coincidence.delta_bar("AAABBBCCC", 3) == 0.0

        # https://en.wikipedia.org/wiki/Index_of_coincidence#Example
        text = uppercase_only("""
            QPWKA LVRXC QZIKG RBPFA EOMFL  JMSDZ VDHXC XJYEB IMTRQ WNMEA
            IZRVK CVKVL XNEIC FZPZC ZZHKM  LVZVZ IZRRQ WDKEC HOSNY XXLSP
            MYKVQ XJTDC IOMEE XDQVS RXLRL  KZHOV""")
        expected_delta_bars = {
            1: 1.12,
            2: 1.19,
            3: 1.05,
            4: 1.17,
            5: 1.82,
            6: 0.99,
            7: 1.00,
            8: 1.05,
            9: 1.17,
            10: 2.07,
        }
        for modulus, expected in expected_delta_bars.items():
            assert coincidence.delta_bar(
                uppercase_only(text), modulus
            ) == pytest.approx(expected, abs=0.01)
