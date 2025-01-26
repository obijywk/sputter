"""Example program to crack a Vigenere cipher."""

from sputter.cipher import vigenere_decrypt
from sputter.fitness import QuadgramStatistics
from sputter.mung import uppercase_only
from sputter.optimize import brute_force


def main():
    """Example program to crack a Vigenere cipher."""
    candidates = set()
    with open("/usr/share/dict/words", encoding="utf-8") as f:
        for line in f:
            word = uppercase_only(line.strip())
            if len(word) == 5:
                candidates.add(word)

    qs = QuadgramStatistics()
    ciphertext = "LXFOPVEFRNHR"

    def objective(k):
        return -qs.string_score(vigenere_decrypt(ciphertext, k))

    results = brute_force(objective, candidates)
    for key, score in results:
        print(f"{key:20} {vigenere_decrypt(ciphertext, key)} {score}")


if __name__ == "__main__":
    main()
