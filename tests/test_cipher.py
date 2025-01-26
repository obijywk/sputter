"""Tests for the cipher module."""

import unittest

from sputter import cipher


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
        self.assertEqual(cipher.caesar_shift("FUS ION", 6), "LAY OUT")
        self.assertEqual(cipher.caesar_shift("LAYOUT", -6), "FUSION")

    def test_substitution(self):
        """Test the substitution cipher implementation."""
        key = cipher.substitution_generate_random_key()
        self.assertEqual(len(key), 26)
        self.assertEqual(len(set(key)), 26)
        ciphertext = cipher.substitution_encrypt("FLEE AT ONCE", key)
        self.assertEqual(cipher.substitution_decrypt(ciphertext, key), "FLEE AT ONCE")

    def test_substitution_permute_key(self):
        """Test the substitution cipher key permutation function."""
        key = cipher.substitution_generate_random_key()
        self.assertEqual(len(key), 26)
        self.assertEqual(len(set(key)), 26)

        permuted_key = cipher.substitution_permute_key(key)
        self.assertEqual(len(permuted_key), 26)
        self.assertEqual(len(set(permuted_key)), 26)
        self.assertNotEqual(key, permuted_key)
        self.assertEqual(sorted(list(permuted_key)), sorted(list(key)))
