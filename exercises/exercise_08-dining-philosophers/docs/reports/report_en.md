# English Report — Exercise 8: Dining Philosophers: Deadlock and Starvation under Lottery

## Abstract

استفاده از بلیت برای انتخاب فیلسوفِ مجاز، جلوگیری از بن‌بست و تحلیل محدودیت گرسنگی. This report explains the algorithm, assumptions, implementation path, reproducible evidence, and limitations.

## Problem and method

This exercise uses Lottery Scheduling to choose among philosophers whose two adjacent forks are available at a scheduling decision. To prevent deadlock, at most N−1 philosophers may enter the room, and a philosopher reserves its pair of forks atomically. The model therefore avoids hold-and-wait.

Each philosopher has base tickets. Optional aging raises the effective weight of a philosopher as it waits, increasing its chance of being selected. The five-philosopher experiment schedules three meals per philosopher and records every meal start and finish. Adjacent philosophers must never eat simultaneously.

Lottery, even with aging, does not guarantee deterministic bounded waiting; an arbitrarily long losing sequence remains possible. The finite seeded run demonstrates that this workload completed, not a universal starvation-freedom proof. A hard guarantee requires a deterministic FIFO reservation rule.

## Model and reproducibility

The workload is defined in `shared/experiments.py` and executed by `run_exercise(8)`. The generated `outputs/results.json` is the evidence source for the results figure. Reproducing a seeded trace requires the same code version, input ordering, and seed.

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
