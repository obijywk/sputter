"""A module implementing common ciphers."""

import itertools


ORD_A = ord("A")


def vigenere_encrypt(plaintext: str, key: str) -> str:
    """Encrypt a plaintext using the Vigenere cipher.

    :param plaintext: The plaintext to encrypt.
    :param key: The key to use for encryption. Must only contain alphabetic characters.

    :return: The encrypted ciphertext.
    """
    key_iter = itertools.cycle([ord(c) - ORD_A for c in key.upper()])
    ciphertext = ""
    for c in plaintext.upper():
        if c.isalpha():
            ciphertext += chr((ord(c) - ORD_A + next(key_iter)) % 26 + ORD_A)
        else:
            ciphertext += c
    return ciphertext


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt a ciphertext using the Vigenere cipher.

    :param ciphertext: The ciphertext to decrypt.
    :param key: The key to use for decryption. Must only contain alphabetic characters.

    :return: The decrypted plaintext.
    """
    key_iter = itertools.cycle([ord(c) - ORD_A for c in key.upper()])
    plaintext = ""
    for c in ciphertext.upper():
        if c.isalpha():
            plaintext += chr((ord(c) - ORD_A - next(key_iter)) % 26 + ORD_A)
        else:
            plaintext += c
    return plaintext


def caesar_shift(text: str, shift: int) -> str:
    """Shift a text by a given number of positions in the alphabet."""
    shifted_text = ""
    for c in text.upper():
        if c.isalpha():
            shifted_text += chr((ord(c) - ORD_A + shift) % 26 + ORD_A)
        else:
            shifted_text += c
    return shifted_text
