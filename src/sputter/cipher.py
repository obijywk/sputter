"""A module implementing common ciphers."""

import itertools
import random

__ORD_A = ord("A")


def vigenere_encrypt(plaintext: str, key: str) -> str:
    """Encrypt a plaintext using the Vigenere cipher.

    :param plaintext: The plaintext to encrypt.
    :param key: The key to use for encryption. Must only contain alphabetic characters.

    :return: The encrypted ciphertext.
    """
    key_iter = itertools.cycle([ord(c) - __ORD_A for c in key.upper()])
    ciphertext = ""
    for c in plaintext.upper():
        if c.isalpha():
            ciphertext += chr((ord(c) - __ORD_A + next(key_iter)) % 26 + __ORD_A)
        else:
            ciphertext += c
    return ciphertext


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt a ciphertext using the Vigenere cipher.

    :param ciphertext: The ciphertext to decrypt.
    :param key: The key to use for decryption. Must only contain alphabetic characters.

    :return: The decrypted plaintext.
    """
    key_iter = itertools.cycle([ord(c) - __ORD_A for c in key.upper()])
    plaintext = ""
    for c in ciphertext.upper():
        if c.isalpha():
            plaintext += chr((ord(c) - __ORD_A - next(key_iter)) % 26 + __ORD_A)
        else:
            plaintext += c
    return plaintext


def caesar_shift(text: str, shift: int) -> str:
    """Shift a text by a given number of positions in the alphabet.

    :param text: The text to shift.
    :param shift: The number of positions to shift.

    :return: The shifted text.
    """
    shifted_text = ""
    for c in text.upper():
        if c.isalpha():
            shifted_text += chr((ord(c) - __ORD_A + shift) % 26 + __ORD_A)
        else:
            shifted_text += c
    return shifted_text


def substitution_encrypt(plaintext: str, key: str) -> str:
    """Encrypt a plaintext using a substitution cipher.

    :param plaintext: The plaintext to encrypt.
    :param key: The key to use for encryption. Must be a permutation of the alphabet.

    :return: The encrypted ciphertext.
    """
    ciphertext = ""
    for c in plaintext.upper():
        if c.isalpha():
            ciphertext += key[ord(c) - __ORD_A]
        else:
            ciphertext += c
    return ciphertext


def substitution_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt a ciphertext using a substitution cipher.

    :param ciphertext: The ciphertext to decrypt.
    :param key: The key to use for decryption. Must be a permutation of the alphabet.

    :return: The decrypted plaintext.
    """
    plaintext = ""
    for c in ciphertext.upper():
        if c.isalpha():
            plaintext += chr(key.index(c) + __ORD_A)
        else:
            plaintext += c
    return plaintext


def substitution_generate_random_key() -> str:
    """Generate a random key for a substitution cipher.

    :return: A random permutation of the alphabet.
    """
    key_list = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    random.shuffle(key_list)
    return "".join(key_list)
