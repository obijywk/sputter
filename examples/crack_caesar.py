"""Example program to crack a Caesar cipher."""

from sputter.cipher import caesar_shift
from sputter.fitness import QuadgramStatistics
from sputter.mung import uppercase_only
from sputter.optimize import brute_force


def main():
    """Example program to crack a Caesar cipher."""
    qs = QuadgramStatistics()
    ciphertext = "QEB NRFZH YOLTK CLU GRJMP LSBO QEB IXWV ALD"
    ciphertext_no_spaces = uppercase_only(ciphertext)

    def objective(shift):
        return -qs.string_score(caesar_shift(ciphertext_no_spaces, shift))

    results = brute_force(objective, range(26))
    for shift, score in results:
        print(f"{shift:02} {caesar_shift(ciphertext, shift)} {score}")


if __name__ == "__main__":
    main()
