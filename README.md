# Lottery Scheduling — Complete Course Exercise Project

A structured, reproducible Python project built around **Lottery Scheduling**. All course exercises are kept together on one branch, with one independent folder per exercise and a shared scheduler implementation to avoid duplicated or inconsistent algorithms.

> **Scope statement:** the discrete-event simulator is an educational model. The `file.py` process controller is a best-effort user-space demonstration based on `psutil`; neither is an operating-system kernel scheduler, and neither offers hard real-time guarantees.

## Start here

- [Project index](PROJECT_INDEX.md) — exercise map and branch link.
- [Project progress and audit](PROJECT_PROGRESS.md) — inspected files, deliverables, tests, limitations.
- [Shared Lottery engine](shared/lottery_scheduler.py) — reproducible weighted draw, discrete scheduler, EDF/RM references, fairness experiments.

## Exercises

| Exercise | Topic | Folder |
|---:|---|---|
| 1 | Introduction, ticket intervals and probability | `exercises/exercise_01-introduction/` |
| 2 | Lottery vs EDF and RM | `exercises/exercise_02-lottery-vs-edf-rm/` |
| 3 | Hand-worked draws and schedule table | `exercises/exercise_03-manual-lottery-trace/` |
| 4 | Synchronization: semaphore, monitor and shared state | `exercises/exercise_04-synchronization-primitives/` |
| 5 | Lottery synchronization demo and trace animation | `exercises/exercise_05-lottery-synchronization-demo/` |
| 6 | Research paper and seminar | `exercises/exercise_06-research-paper-seminar/` |
| 7 | Readers-writers fairness | `exercises/exercise_07-readers-writers/` |
| 8* | Dining philosophers: deadlock and starvation | `exercises/exercise_08-dining-philosophers/` |

`*` Exercise 8 is included as an additional folder because it was also requested in the earlier course work. The uploaded project brief specifies seven exercises; therefore the first seven constitute its stated scope, while Exercise 8 is explicitly marked as an extra known assignment.

## Install and run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

# Run every exercise experiment
python tools/run_all_exercises.py

# Rebuild figures and presentation
python tools/generate_figures.py
python tools/build_seminar.py

# Run the full test suite
python -m pytest -q
```

Run one exercise from the repository root, for example:

```bash
python exercises/exercise_01-introduction/src/run.py
```

Each exercise folder has its own `README.md`, `src/`, `tests/`, `docs/README.md`, `docs/figures/`, Persian and English Markdown reports, and `outputs/`.

## Core Lottery rule

For a ready set R, let T be the sum of all ticket counts. Draw an integer r uniformly from 1..T. The first cumulative ticket interval containing r wins one CPU quantum (or the remaining execution time when shorter). Thus:

`P(task i wins one draw) = tickets(i) / sum(tickets of ready tasks)`.

The expected share is probabilistic and becomes more representative over repeated draws. No exact short-window share, deadline guarantee, or deterministic starvation bound follows from the base algorithm.

## Validation

All result plots are generated from the JSON outputs created by the experiment scripts. The seeded simulator makes those outputs repeatable. The `psutil` process runner is deliberately described separately because real process suspension is OS-dependent and only approximates a user-space scheduler.

## References

- Waldspurger, C. A., & Weihl, W. E. (1994). *Lottery Scheduling: Flexible Proportional-Share Resource Management*. OSDI '94. [USENIX paper page](https://www.usenix.org/conference/osdi-94/lottery-scheduling-flexible-proportional-share-resource-management).
- Waldspurger, C. A. (1995). *Lottery and Stride Scheduling: Flexible Proportional-share Resource Management*. MIT Ph.D. thesis. [MIT DSpace record](https://dspace.mit.edu/entities/publication/bdf65551-de4e-46b4-8f8d-9e89da6c01b4).
