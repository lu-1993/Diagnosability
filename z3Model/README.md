# How to run

Ask for the help is a good starting point.

```python3
./main.py -h
usage: main.py [-h] --method {kDiag,lDiag} [--symmetry] [--recar] file

Diagnosis tool

positional arguments:
  file                  The input file path.

optional arguments:
  -h, --help            show this help message and exit
  --method {kDiag,lDiag}
                        Which kind of dignosis process we want to use
  --symmetry            Is the symmetry breaking constraints have been added?
  --recar               Is the RECAR mode activated?
```

If we want to run the k diagnosability without symmetry on the formula stored
input.txt:

```python3
./main.py --method kDiag input.txt
```
