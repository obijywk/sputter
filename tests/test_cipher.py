"""Tests for the cipher module."""

import unittest

from texput import cipher


class CipherTestCase(unittest.TestCase):
    """Tests for the cipher module."""

    def test_vigenere(self):
        """Test the Vigenere cipher implementation."""
        self.assertEqual(cipher.vigenere_encrypt("ABC", "B"), "BCD")
        self.assertEqual(cipher.vigenere_encrypt("ABC DEF", "B"), "BCD EFG")
        self.assertEqual(cipher.vigenere_encrypt("XYZ", "B"), "YZA")
        self.assertEqual(
            cipher.vigenere_encrypt("ATTACKATDAWN", "LEMON"), "LXFOPVEFRNHR"
        )

        self.assertEqual(cipher.vigenere_decrypt("BCD", "B"), "ABC")
        self.assertEqual(cipher.vigenere_decrypt("BCD EFG", "B"), "ABC DEF")
        self.assertEqual(cipher.vigenere_decrypt("YZA", "B"), "XYZ")
        self.assertEqual(
            cipher.vigenere_decrypt("LXFOPVEFRNHR", "LEMON"), "ATTACKATDAWN"
        )

    def test_caesar(self):
        """Test the Caesar shift implementation."""
        self.assertEqual(cipher.caesar_shift("FUSION", 6), "LAYOUT")
        self.assertEqual(cipher.caesar_shift("LAYOUT", -6), "FUSION")
