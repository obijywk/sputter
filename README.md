# sputter

sputter is a Statistical PUzzle TexT procEssoR. It is a Python library that can
be used for many kinds of cryptanalysis and text transformation tasks that are
often helpful when solving puzzle hunts.

## Documentation

You may refer to the generated [API documentation](https://obijywk.github.io/sputter/).

## Example usages

The sputter command line tool serves as an example of how to use the sputter
library, and may also be useful on its own, as demonstrated by the examples
below.

```
$ uv run sputter crack-caesar 'QEB NRFZH YOLTK CLU GRJMP LSBO QEB IXWV ALD'
  358.79 03 THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG
  558.25 23 NBY KOCWE VLIQH ZIR DOGJM IPYL NBY FUTS XIA
  566.45 07 XLI UYMGO FVSAR JSB NYQTW SZIV XLI PEDC HSK
  567.31 13 DRO AESMU LBYGX PYH TEWZC YFOB DRO VKJI NYQ
  568.09 19 JXU GKYSA RHEMD VEN ZKCFI ELUH JXU BQPO TEW
```

```
$ uv run sputter crack-substitution 'IDTG GYPIYPCY EJUY FB VL QYHJITRYHW CVEEVP YPOHTGD SVQUG TG FGYU JG J IYGI CJGY LVQ IDY GFNGITIFITVP CTBDYQ CQJCXYQ'
  161.51 JNCUYLODTZXHEPVBKQGIFRSAWM THIS SENTENCE MADE UP OF RELATIVELY COMMON ENGLISH WORDS IS USED AS A TEST CASE FOR THE SUBSTITUTION CIPHER CRACKER
  161.51 JNCUYLODTMXHEPVBKQGIFRSAWZ THIS SENTENCE MADE UP OF RELATIVELY COMMON ENGLISH WORDS IS USED AS A TEST CASE FOR THE SUBSTITUTION CIPHER CRACKER
  161.51 JNCUYLODTAXHEPVBKQGIFRSMWZ THIS SENTENCE MADE UP OF RELATIVELY COMMON ENGLISH WORDS IS USED AS A TEST CASE FOR THE SUBSTITUTION CIPHER CRACKER
  161.51 JNCUYLODTAXHEPVBMQGIFRSKWZ THIS SENTENCE MADE UP OF RELATIVELY COMMON ENGLISH WORDS IS USED AS A TEST CASE FOR THE SUBSTITUTION CIPHER CRACKER
  161.51 JNCUYLODTKXHEPVBMQGIFRSAWZ THIS SENTENCE MADE UP OF RELATIVELY COMMON ENGLISH WORDS IS USED AS A TEST CASE FOR THE SUBSTITUTION CIPHER CRACKER
```

```
$ uv run sputter crack-vigenere --key-length 5 LXFOPVEFRNHR
Will attempt to decrypt with key lengths: [5]
   99.96 HENNY ETSBROASEPAN
  100.03 LEMON ATTACKATDAWN
  103.73 DIRAC IPOONSWORLEJ
  105.65 DECOR ITDAYSADDWEN
  108.96 DENNY ITSBRSASEPEN
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
$ uv run sputter reorder -e "4 2 1 4 2 3 7 7" AND ATE ERC ERE FTH OMM ORD SIS STO THI
   64.87 THIS IS A TEST OF THE REORDER COMMAND
   73.25 THIS IS E REST OF THE RCORDOM MANDATE
   75.99 THIS IS A TEST OF THO RDEREER COMMAND
   76.78 THIS IS F THAT ES TOO RDEREER COMMAND
   78.46 THIS IS E REST OF THA TEORDER COMMAND
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
