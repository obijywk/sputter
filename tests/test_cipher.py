"""Tests for the cipher module."""

import unittest

from sputter import cipher


class CipherTestCase(unittest.TestCase):
    """Tests for the cipher module."""

    def test_vigenere(self):
        """Test the Vigenere cipher implementation."""
        assert cipher.vigenere_encrypt("ABC", "B") == "BCD"
        assert cipher.vigenere_encrypt("ABC DEF", "B") == "BCD EFG"
        assert cipher.vigenere_encrypt("XYZ", "B") == "YZA"
        assert cipher.vigenere_encrypt("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"

        assert cipher.vigenere_decrypt("BCD", "B") == "ABC"
        assert cipher.vigenere_decrypt("BCD EFG", "B") == "ABC DEF"
        assert cipher.vigenere_decrypt("YZA", "B") == "XYZ"
        assert cipher.vigenere_decrypt("LXFOPVEFRNHR", "LEMON") == "ATTACKATDAWN"

    def test_caesar(self):
        """Test the Caesar shift implementation."""
        assert cipher.caesar_shift("FUS ION", 6) == "LAY OUT"
        assert cipher.caesar_shift("LAYOUT", -6) == "FUSION"

    def test_substitution(self):
        """Test the substitution cipher implementation."""
        key = cipher.substitution_generate_random_key()
        assert len(key) == 26
        assert len(set(key)) == 26
        ciphertext = cipher.substitution_encrypt("FLEE AT ONCE", key)
        assert cipher.substitution_decrypt(ciphertext, key) == "FLEE AT ONCE"
