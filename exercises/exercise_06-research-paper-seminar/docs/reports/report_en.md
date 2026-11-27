# English Report — Exercise 6: Research Paper and Seminar on Lottery Scheduling

## Abstract

تحلیل مقالهٔ اصلی Waldspurger و Weihl، مزایا، currency، ticket transfer، محدودیت‌ها و ارائهٔ کلاسی. This report explains the algorithm, assumptions, implementation path, reproducible evidence, and limitations.

## Problem and method

This exercise reviews the original Lottery Scheduling paper by Carl A. Waldspurger and William E. Weihl, presented at OSDI 1994. The paper describes randomized proportional-share resource management and discusses abstractions such as ticket currencies and extensions to I/O bandwidth, memory, and locks.

The report explains the base ticket model, then separates research extensions—ticket transfer, ticket currencies, and compensation tickets—from the simpler implementation in this repository. The code here implements weighted lotteries; it does not claim to implement the paper's full system.

The research conclusion distinguishes proportional resource allocation from hard real-time deadline guarantees. A seminar deck summarizes the problem, model, pseudocode, reproducible experiment, and limitations.

## Model and reproducibility

The workload is defined in `shared/experiments.py` and executed by `run_exercise(6)`. The generated `outputs/results.json` is the evidence source for the results figure. Reproducing a seeded trace requires the same code version, input ordering, and seed.

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
