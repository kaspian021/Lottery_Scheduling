# Project Progress — Lottery Scheduling All Exercises

## Repository inspection (before edits)

- Default branch: `main`.
- Existing branches: `main`, `master`, `Exercise5`.
- Default-branch tree contained only `Readme.md` and `file.py`.
- Existing README described its sample chart and ten-slot schedule as illustrative, not measured output.
- README referred to `lottery_gantt_animation.mp4` and `.gif`, but neither file existed in the default-branch tree.
- `file.py` used `subprocess.Popen`, `psutil` suspend/resume and `random.choices`; there was no dependency manifest, test suite, scenario folder, docs folder, or output directory.
- No DOCX/PDF report files existed in the inspected default branch.

## Scope and interpretation

The attached work brief says seven exercises, while previous course context also included Exercise 8 (Dining Philosophers). The implementation therefore contains eight folders: Exercises 1–7 form the requested seven-exercise set, and Exercise 8 is clearly labelled as an additional task.

## Implemented on this branch

- One shared Lottery Scheduling engine with seeded random draws, ticket intervals, discrete CPU quanta, waiting/response/turnaround metrics, and EDF/RM comparison references.
- Best-effort `psutil` process runner with input validation and cleanup; it is explicitly not represented as kernel scheduling.
- One folder per exercise, each with README, source runner, tests, docs guide, 2 SVG figures, 1 generated PNG plot, Persian/English report sources, and JSON results.
- Exercise 4 synchronization comparison (Semaphore and Condition/Monitor).
- Exercise 5 synchronization trace and result chart generated from executed results. The current branch does not include a GIF animation.
- Exercise 6 research report and seminar slide deck based on the primary 1994 paper.
- Exercise 7 phase-based readers-writers model.
- Exercise 8 dining-philosophers model with N-1 admission, atomic pair reservation, ticket aging, and explicit statement that aging does not prove bounded waiting.
- Root project index, instructions, reproducibility tooling, requirements, and a build workflow. A separate read-only CI workflow is also provided.

## Validation

See `outputs/test_results.txt` and each exercise's `outputs/results.json`. Figures are generated from these JSON files. The project-level test command is `python -m pytest -q`.

## Known limits

- The seven-exercise assignment brief did not include the professor's individual exercise titles or the original grading table. Exercise mapping follows the prior course exercise set already discussed in this project. If the professor's original titles differ, this folder mapping may need adjustment.
- The main scheduler is a discrete-event teaching model with integer ticks, single CPU and no context-switch cost or I/O blocking.
- Lottery Scheduling cannot promise deterministic deadline satisfaction or bounded waiting.
- The external process runner suspends user-space processes using `psutil`. It is platform dependent, does not control the kernel, and process-tree behavior or startup races can affect precision.
- The readers-writers and dining-philosophers exercises are finite-state/trace models, not formal proofs for every thread interleaving.
