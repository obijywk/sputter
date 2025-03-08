"""The sputter command line tool."""

from sputter.cipher import (
    caesar_shift,
    substitution_decrypt,
    substitution_generate_random_key,
    vigenere_decrypt,
)
from sputter.fitness import QuadgramStatistics, WordStatistics
from sputter.mung import (
    randomly_swap_letters,
    uppercase_and_spaces_only,
    uppercase_only,
)
from sputter.optimize import brute_force, simulated_annealing, SimulatedAnnealingConfig
import sputter.unweaver as unweaver
from sputter.word_features import WordFeatureStatistics

import rich
from rich.console import Console
import typer
from typing import List, Optional


app = typer.Typer()
console = Console()


@app.command()
def crack_caesar(ciphertext: str, num_results: Optional[int] = 5):
    """Crack a ciphertext encrypted with a Caesar cipher."""
    qs = QuadgramStatistics()
    ciphertext_no_spaces = uppercase_only(ciphertext)

    def objective(shift):
        return -qs.string_score(caesar_shift(ciphertext_no_spaces, shift))

    results = brute_force(objective, range(26), top_n=num_results)
    for shift, score in results:
        rich.print(f"{shift:02} {caesar_shift(ciphertext, shift)} {score}")


@app.command()
def crack_substitution(ciphertext: str, num_results: Optional[int] = 5):
    """Crack a ciphertext encrypted with a substitution cipher."""
    ws = WordStatistics()

    ciphertext = uppercase_and_spaces_only(ciphertext)

    def objective(key):
        return -ws.spaced_string_score(substitution_decrypt(ciphertext, key))

    with console.status("Searching...") as status:

        def progress_callback(
            temperature: float, state: str, state_score: float
        ) -> None:
            status.update(f"{temperature:10.2f} {state} {state_score:6.2f}")

        results = simulated_annealing(
            objective,
            substitution_generate_random_key(),
            randomly_swap_letters,
            top_n=num_results,
            config=SimulatedAnnealingConfig(
                progress_callback=progress_callback,
            ),
        )

    for key, score in results:
        rich.print(f"{key} {score:6.2f} {substitution_decrypt(ciphertext, key)}")


@app.command()
def crack_vigenere(key_length: int, ciphertext: str, num_results: Optional[int] = 5):
    """Crack a ciphertext encrypted with a Vigenere cipher."""
    ws = WordStatistics()
    key_candidates = [w for w in ws.word_frequencies() if len(w) == key_length]

    qs = QuadgramStatistics()

    def objective(k):
        return -qs.string_score(vigenere_decrypt(ciphertext, k))

    results = brute_force(objective, key_candidates, top_n=num_results)
    for key, score in results:
        rich.print(f"{key} {vigenere_decrypt(ciphertext, key)} {score}")


@app.command()
def evaluate_word_features(words: List[str], num_results: Optional[int] = 5):
    """Detect statistically interesting features in a set of words."""
    words = [uppercase_only(w) for w in words]
    with console.status("Computing corpus word feature statistics...") as status:
        wfs = WordFeatureStatistics()
        status.update("Computing feature likelihood for input words...")
        results = wfs.evaluate_words(words, top_n=num_results)
    for result in results:
        rich.print(f"{result.log_prob:10.2f} {result.feature} {result.words}")


@app.command()
def unweave(
    text: str,
    min_words: Optional[int] = None,
    max_words: Optional[int] = None,
    num_results: Optional[int] = 5,
):
    """Separate words that have been "interwoven" into a single ordered sequence."""
    config = unweaver.Config(min_words=min_words, max_words=max_words)
    with console.status("Unweaving..."):
        results = unweaver.unweave(text, top_n=num_results, config=config)
    for words, score in results:
        rich.print(f"{score:10.2f} {words}")


if __name__ == "__main__":
    app()
