"""Example program to crack a Caesar cipher."""

from texput.cipher import caesar_shift
from texput.fitness import QuadgramStatistics
from texput.mung import uppercase_only
from texput.optimize import brute_force


def main():
    """Example program to crack a Caesar cipher."""
    qs = QuadgramStatistics()
    ciphertext = "QEB NRFZH YOLTK CLU GRJMP LSBO QEB IXWV ALD"
    ciphertext_no_spaces = uppercase_only(ciphertext)

    def objective(shift):
        return qs.string_score(caesar_shift(ciphertext_no_spaces, shift))

    results = brute_force(objective, range(26))
    for shift, score in results:
        print(f"{shift:02} {caesar_shift(ciphertext, shift)} {score}")


if __name__ == "__main__":
    main()
