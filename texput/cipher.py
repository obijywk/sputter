"""A module implementing common ciphers."""

import itertools


def vigenere_encrypt(plaintext: str, key: str) -> str:
    """Encrypt a plaintext using the Vigenere cipher.

    :param plaintext: The plaintext to encrypt.
    :param key: The key to use for encryption. Must only contain alphabetic characters.

    :return: The encrypted ciphertext.
    """
    key_iter = itertools.cycle([ord(c) - ord("A") for c in key.upper()])
    ciphertext = ""
    for c in plaintext.upper():
        if c.isalpha():
            ciphertext += chr((ord(c) - ord("A") + next(key_iter)) % 26 + ord("A"))
        else:
            ciphertext += c
    return ciphertext


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt a ciphertext using the Vigenere cipher.

    :param ciphertext: The ciphertext to decrypt.
    :param key: The key to use for decryption. Must only contain alphabetic characters.

    :return: The decrypted plaintext.
    """
    key_iter = itertools.cycle([ord(c) - ord("A") for c in key.upper()])
    plaintext = ""
    for c in ciphertext.upper():
        if c.isalpha():
            plaintext += chr((ord(c) - ord("A") - next(key_iter)) % 26 + ord("A"))
        else:
            plaintext += c
    return plaintext
