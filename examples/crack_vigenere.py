from texput.cipher import vigenere_decrypt
from texput.fitness import QuadgramStatistics
from texput.mung import uppercase_only
from texput.optimize import brute_force

if __name__ == "__main__":
    candidates = set()
    with open("/usr/share/dict/words") as f:
        for line in f:
            word = uppercase_only(line.strip())
            if len(word) == 5:
                candidates.add(word)
    
    qs = QuadgramStatistics()
    ciphertext = "LXFOPVEFRNHR"
    objective = lambda k: qs.string_score(vigenere_decrypt(ciphertext, k))
    results = brute_force(objective, candidates)
    for key, score in results:
        print(f"{key:20} {vigenere_decrypt(ciphertext, key)} {score}")