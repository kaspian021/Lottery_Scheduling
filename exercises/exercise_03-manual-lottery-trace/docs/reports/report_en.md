# English Report — Exercise 3: Hand-worked Lottery Draws and Trace Table

## Abstract

This report explains how ticket intervals map a random draw to a winner, how the selected jobs are ordered, and how observed shares are interpreted. It also documents the model assumptions, implementation path, reproducible evidence, and limitations.

## Problem and method

This exercise turns the lottery selection into a paper-checkable table. With P1=5, P2=3, and P3=2, the total is ten tickets. Cumulative intervals are 1–5 for P1, 6–8 for P2, and 9–10 for P3. The interval containing the winning integer identifies the selected process.

The program generates 15 draws with seed 7 and records the decision number, random ticket, total tickets, winner, and winning interval. Reproducing the exact sequence requires the same seed and process ordering. A different seed produces a different valid sequence.

Observed share is the number of wins divided by the number of draws. A 15-draw sample naturally varies from the theoretical 50/30/20 proportions; the table is not a deterministic CPU-share guarantee.

## Model and reproducibility

The workload is defined in `shared/experiments.py` and executed by `run_exercise(3)`. The generated `outputs/results.json` is the evidence source for the results figure. Reproducing a seeded trace requires the same code version, input ordering, and seed.

## Lottery pseudocode

```text
while unfinished jobs exist:
    ready = arrived jobs with remaining work
    if ready is empty: advance to the next arrival
    T = sum tickets among ready jobs
    r = uniform integer in [1, T]
    winner = job whose cumulative ticket interval contains r
    execute winner for one quantum or until completion
    update response, waiting, remaining work, and finish time
```

## Figures and interpretation

`figures/architecture.svg` documents the model components. `figures/flowchart.svg` shows the decision path. `figures/results.png` is generated from the experiment JSON rather than manually authored numbers.

## Validation and limitations

Tests verify input validation, completion, reproducibility, and the exercise-specific invariants. Ticket weights control expected shares over repeated draws; they do not guarantee an exact short-run share or a hard deadline. This repository is an educational user-space model, not a kernel scheduler.

## Reference

Waldspurger, C. A., & Weihl, W. E. (1994). *Lottery Scheduling: Flexible Proportional-Share Resource Management*. OSDI '94. https://www.usenix.org/conference/osdi-94/lottery-scheduling-flexible-proportional-share-resource-management
## Complete hand-checkable draw table

The table is read directly from `outputs/results.json` using seed=7. Both interval endpoints are inclusive.

| Decision | Draw | Total tickets | Winner | Winning interval |
|---:|---:|---:|---|---:|
| 1 | 6 | 10 | P2 | 6–8 |
| 2 | 3 | 10 | P1 | 1–5 |
| 3 | 7 | 10 | P2 | 6–8 |
| 4 | 1 | 10 | P1 | 1–5 |
| 5 | 2 | 10 | P1 | 1–5 |
| 6 | 9 | 10 | P3 | 9–10 |
| 7 | 2 | 10 | P1 | 1–5 |
| 8 | 6 | 10 | P2 | 6–8 |
| 9 | 10 | 10 | P3 | 9–10 |
| 10 | 1 | 10 | P1 | 1–5 |
| 11 | 9 | 10 | P3 | 9–10 |
| 12 | 4 | 10 | P1 | 1–5 |
| 13 | 1 | 10 | P1 | 1–5 |
| 14 | 2 | 10 | P1 | 1–5 |
| 15 | 7 | 10 | P2 | 6–8 |

A spreadsheet-friendly copy is stored at `outputs/manual_draws.csv`. This is one reproducible trace, not a guaranteed sequence for every seed.
