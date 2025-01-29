"""Example program to crack a simple substitution cipher."""

from sputter.cipher import (
    substitution_encrypt,
    substitution_decrypt,
    substitution_generate_random_key,
)
from sputter.fitness import WordStatistics
from sputter.mung import randomly_swap_letters, uppercase_and_spaces_only
from sputter.optimize import SimulatedAnnealingConfig, simulated_annealing


def main():
    """Example program to crack a simple substitution cipher."""
    plaintext = uppercase_and_spaces_only(
        """
        Yesterday
        All my troubles seemed so far away
        Now it looks as though they're here to stay
        Oh, I believe in yesterday"""
    )
    correct_key = substitution_generate_random_key()
    ciphertext = substitution_encrypt(plaintext, correct_key)

    ws = WordStatistics()

    def objective(key):
        return -ws.spaced_string_score(substitution_decrypt(ciphertext, key))

    print("Target score: ", objective(correct_key))

    def progress_callback(temperature: float, state: str, state_score: float):
        print(f"{temperature:10.2f} {state} {state_score:6.2f}")

    results = simulated_annealing(
        objective,
        substitution_generate_random_key(),
        randomly_swap_letters,
        config=SimulatedAnnealingConfig(
            progress_callback=progress_callback,
        ),
    )

    for key, score in results:
        print(f"{key} {score:6.2f} {substitution_decrypt(ciphertext, key)}")


if __name__ == "__main__":
    main()
