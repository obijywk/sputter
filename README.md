# sputter

sputter is a Statistical PUzzle TexT procEssoR. It is a Python library that can
be used for many kinds of cryptanalysis and text transformation tasks that are
often helpful when solving puzzle hunts.

## Example usages

The sputter command line tool serves as an example of how to use the sputter
library, and may also be useful on its own, as demonstrated by the examples
below.

```
$ uv run sputter crack-caesar 'QEB NRFZH YOLTK CLU GRJMP LSBO QEB IXWV ALD'
03 THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG 358.7871900461235
23 NBY KOCWE VLIQH ZIR DOGJM IPYL NBY FUTS XIA 558.2539523522809
07 XLI UYMGO FVSAR JSB NYQTW SZIV XLI PEDC HSK 566.445149039387
13 DRO AESMU LBYGX PYH TEWZC YFOB DRO VKJI NYQ 567.3074406217602
19 JXU GKYSA RHEMD VEN ZKCFI ELUH JXU BQPO TEW 568.091701966427
```

```
$ uv run sputter crack-substitution 'IDTG GYPIYPCY EJUY FB VL QYHJITRYHW CVEEVP YPOHTGD SVQUG TG FGYU JG J IYGI CJGY LVQ IDY GFNGITIFITVP CTBDYQ CQJCXYQ'
JNCUYLODTAXHEPVBMQGIFRSKWZ 161.51 THIS SENTENCE MADE UP OF RELATIVELY COMMON ENGLISH WORDS IS USED AS A TEST CASE FOR THE SUBSTITUTION CIPHER CRACKER
JNCUYLODTAXHEPVBKQGIFRSMWZ 161.51 THIS SENTENCE MADE UP OF RELATIVELY COMMON ENGLISH WORDS IS USED AS A TEST CASE FOR THE SUBSTITUTION CIPHER CRACKER
JNCUYLODTAXHEPVBMQGIFRSKWZ 161.51 THIS SENTENCE MADE UP OF RELATIVELY COMMON ENGLISH WORDS IS USED AS A TEST CASE FOR THE SUBSTITUTION CIPHER CRACKER
JNCUYLODTMXHEPVBAQGIFRSZWK 161.51 THIS SENTENCE MADE UP OF RELATIVELY COMMON ENGLISH WORDS IS USED AS A TEST CASE FOR THE SUBSTITUTION CIPHER CRACKER
JNCUYLODTKXHEPVBAQGIFRSZWM 161.51 THIS SENTENCE MADE UP OF RELATIVELY COMMON ENGLISH WORDS IS USED AS A TEST CASE FOR THE SUBSTITUTION CIPHER CRACKER
```

```
$ uv run sputter crack-vigenere 5 LXFOPVEFRNHR
HENNY ETSBROASEPAN 99.96089810813712
LEMON ATTACKATDAWN 100.0337193614982
DIRAC IPOONSWORLEJ 103.72768482103916
DECOR ITDAYSADDWEN 105.64900698963312
DENNY ITSBRSASEPEN 108.95957454786881
```

```
$ uv run sputter evaluate-word-features STEPSISTERS ERNIEELS SINNFEIN NINEONEONE SUSPENDEDSENTENCE
    -26.62 at least 5 cardinal directions ['STEPSISTERS', 'ERNIEELS', 'SINNFEIN', 'NINEONEONE', 'SUSPENDEDSENTENCE']
    -20.31 at least 3 occurrences of N ['SINNFEIN', 'NINEONEONE', 'SUSPENDEDSENTENCE']
    -19.39 at least 4 cardinal directions ['STEPSISTERS', 'ERNIEELS', 'SINNFEIN', 'NINEONEONE', 'SUSPENDEDSENTENCE']
    -15.15 at least 3 occurrences of E ['ERNIEELS', 'NINEONEONE', 'SUSPENDEDSENTENCE']
    -12.76 at least 3 occurrences of S ['STEPSISTERS', 'SUSPENDEDSENTENCE']
```

```
$ uv run sputter unweave --max-words=5 TFMTHUREUOSDRISNDDDAAAYAYYY
     42.03 ['THURSDAY', 'FRIDAY', 'MONDAY', 'TUESDAY']
     50.53 ['THURSDAY', 'FRIDAY', 'MON', 'TUESDAY', 'DAY']
     53.99 ['THURSDAY', 'FRI', 'MONDAY', 'TUESDAY', 'DAY']
     54.73 ['THURSDAY', 'FRIDA', 'MONDAY', 'TUESDAY', 'Y']
     55.60 ['THUDS', 'FRIDAY', 'MORNAY', 'TUESDAY', 'DAY']
```

## Development instructions

Install [uv](https://github.com/astral-sh/uv).

Install the [pre-commit](https://pre-commit.com/) hooks:
```
$ uv run pre-commit install
```

Run tests:
```
$ uv run pytest
```

Run code coverage:
```
$ uv run coverage run -m pytest
$ uv run coverage report
$ uv run coverage html
```

Run linter and code formatter:
```
$ uv run ruff check
$ uv run ruff format
```

Build documentation:
```
$ uv run pdoc --output-dir=docs src/sputter
```

Run all pre-commits:
```
$ uv run pre-commit run --all-files
```

## Acknowledgments

The word_features module was inspired by (and is more-or-less a Python port of) the [Collective.jl](https://github.com/rdeits/Collective.jl) library by [Robin Deits](https://github.com/rdeits).
