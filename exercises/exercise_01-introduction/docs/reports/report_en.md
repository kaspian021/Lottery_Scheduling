# English Report — Exercise 1: Lottery Scheduling: Algorithm and Ticket Model

## Abstract

معرفی زمان‌بندی قرعه‌کشی، فضای بلیت‌ها، احتمال انتخاب و سهم مورد انتظار پردازنده. This report explains the algorithm, assumptions, implementation path, reproducible evidence, and limitations.

## Problem and method

This exercise introduces Lottery Scheduling as a randomized proportional-share policy. Each runnable task owns tickets. A uniform integer is drawn from one through the sum of runnable tickets, and cumulative ticket intervals identify the winner. Task i wins a single draw with probability t_i divided by the total runnable tickets.

The baseline pool assigns five tickets to P1, three to P2, and two to P3, yielding expected shares of 50%, 30%, and 20%. The experiment runs 10,000 draws with a fixed seed. Observed shares are compared with theoretical shares and sampling error is reported. A short run is not expected to match the target exactly.

The repository provides a discrete-time educational simulator and a separate best-effort user-space process runner. Neither should be described as a kernel scheduler. The simulator makes its workload, seed, quantum, and assumptions explicit so results can be reproduced.

## Model and reproducibility

The workload is defined in `shared/experiments.py` and executed by `run_exercise(1)`. The generated `outputs/results.json` is the evidence source for the results figure. Reproducing a seeded trace requires the same code version, input ordering, and seed.

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
