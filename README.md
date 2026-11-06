# Exercise 5 — Lottery Scheduling with Synchronization

This exercise compares three Lottery Scheduling variants:

1. **Lottery with Semaphore** — a binary semaphore guards scheduler state.
2. **Lottery with Monitor** — a `threading.Condition` provides monitor-style mutual exclusion and notification.
3. **Lottery with Semaphore and Monitor** — both guards are used, always acquiring the semaphore before the condition lock.

## Scheduling rules
- Every process has a positive number of tickets.
- Each scheduling decision draws one ticket uniformly from all tickets belonging to ready processes.
- The winning process runs for `min(quantum, remaining burst)`.
- Ticket counts influence the probability of being selected; they do not guarantee strict order.
- This is a deterministic-seedable **simulation** and does not suspend or launch real external programs.

## Run from this folder
```bash
python lottery_sync_demo.py --mode semaphore --gantt gantt-semaphore.svg
python lottery_sync_demo.py --mode monitor --gantt gantt-monitor.svg
python lottery_sync_demo.py --mode both --gantt gantt-both.svg
python lottery_sync_demo.py --all --gantt gantt.svg
```

## Run tests
```bash
python -m unittest discover -s . -p 'test_*.py' -v
```

## Sample processes
| Process | Arrival | CPU burst | Tickets |
|---|---:|---:|---:|
| P1 | 0 | 5 | 5 |
| P2 | 0 | 3 | 3 |
| P3 | 0 | 4 | 2 |
| P4 | 1 | 2 | 1 |
| P5 | 2 | 3 | 4 |

## Flowchart
```text
START -> Initialize processes, ticket counts, quantum and seed
      -> Choose semaphore / monitor / both
      -> Any ready processes?
          NO: advance to next arrival, or END if all finished
          YES: sum ready tickets -> draw random ticket
              -> find process owning ticket -> run one quantum
              -> update remaining burst, Gantt trace and metrics
              -> release guard / notify -> repeat
```

The infographic is in `assets/lottery_sync_comparison.svg`. Use the same seed to compare equivalent traces across synchronization modes.
