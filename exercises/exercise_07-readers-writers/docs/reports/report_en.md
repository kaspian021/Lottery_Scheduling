# English Report — Exercise 7: Readers-Writers with Ticket-Based Phase Arbitration

## Abstract

مقایسهٔ reader-preference، writer-preference و lottery-phase با حفظ انحصار نویسنده. This report explains the algorithm, assumptions, implementation path, reproducible evidence, and limitations.

## Problem and method

The readers-writers problem requires that multiple readers may share access while a writer has exclusive access. This exercise models admission in phases: a reader phase grants a cohort of waiting readers, while a writer phase grants exactly one writer.

Three policies are compared: reader preference, writer preference, and lottery arbitration proportional to the aggregate tickets of waiting readers and writers. In a lottery reader phase, all readers waiting at the phase boundary form a cohort; in a writer phase, one writer is selected by its tickets.

The model preserves writer exclusivity, but randomized selection provides no deterministic bounded-wait guarantee. A finite trace in which every request completes is not a universal starvation-freedom proof.

## Model and reproducibility

The workload is defined in `shared/experiments.py` and executed by `run_exercise(7)`. The generated `outputs/results.json` is the evidence source for the results figure. Reproducing a seeded trace requires the same code version, input ordering, and seed.

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
