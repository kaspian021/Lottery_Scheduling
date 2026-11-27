# English Report — Exercise 2: Lottery vs EDF and RM

## Abstract

مقایسهٔ هدف، قاعدهٔ انتخاب، سهم CPU و deadline miss روی یک workload مشترک. This report explains the algorithm, assumptions, implementation path, reproducible evidence, and limitations.

## Problem and method

This exercise compares three policies on the same single-job workload. Lottery selects runnable work by weighted random draws. EDF selects the ready job with the earliest absolute deadline. RM assigns fixed priority by period, with shorter periods receiving higher priority.

The workload records arrival, execution burst, tickets, deadline, and period. Lottery uses a fixed random seed; the EDF and RM reference schedulers make a preemptive decision at each integer tick. Generated results include Gantt traces, waiting, turnaround, response, and deadline-miss indicators.

Lottery is designed for proportional CPU allocation, not hard deadline guarantees. EDF and RM have real-time objectives and their schedulability claims depend on their respective task and processor assumptions. A small experiment illustrates behavior; it does not establish universal superiority.

## Model and reproducibility

The workload is defined in `shared/experiments.py` and executed by `run_exercise(2)`. The generated `outputs/results.json` is the evidence source for the results figure. Reproducing a seeded trace requires the same code version, input ordering, and seed.

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
