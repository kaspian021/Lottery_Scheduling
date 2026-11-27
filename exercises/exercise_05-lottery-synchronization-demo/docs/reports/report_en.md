# English Report — Exercise 5: Lottery Synchronization Demonstration

## Abstract

ساخت trace و تصویر مرحله‌ای از انتخاب بلیت و حفاظت هم‌زمانی با Semaphore/Monitor. This report explains the algorithm, assumptions, implementation path, reproducible evidence, and limitations.

## Problem and method

This exercise provides a step-by-step Lottery Scheduling demonstration and shows why synchronization is required around the shared draw state. Semaphore and Condition-based monitor variants protect the random draw, interval lookup, and winner counter update.

Generated outputs include completed draw counts, per-group wins, and the trace used by the animation. Thread interleavings can differ between runs, so the stable correctness checks are the completed operation count and shared-state invariants—not a claim that the observed order is a reproducible benchmark.

Lottery defines the selection policy; a semaphore or monitor protects the implementation state. These are complementary layers rather than interchangeable algorithms.

## Model and reproducibility

The workload is defined in `shared/experiments.py` and executed by `run_exercise(5)`. The generated `outputs/results.json` is the evidence source for the results figure. Reproducing a seeded trace requires the same code version, input ordering, and seed.

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
