# Lottery Scheduling — CPU Scheduling Project

## Overview

Lottery Scheduling is a **probabilistic proportional-share CPU scheduling algorithm**. Each runnable process owns a number of tickets. At each scheduling decision, the scheduler draws one ticket uniformly at random; the process that owns the winning ticket receives the next CPU time slice. A process with more tickets has a greater chance of being selected.

> **Project note:** The schedule, ticket draw, and charts in this README are a worked educational example, not measured output from the repository's implementation. Update the example and run instructions to match the source code if they differ.

## How it works

1. Keep track of all runnable processes.
2. Assign each runnable process a positive number of tickets.
3. Compute the total number of tickets, `T`.
4. Draw a uniformly random integer `w` in `[1, T]`.
5. Walk through the processes, accumulating ticket counts until the cumulative count is at least `w`.
6. Run the winning process for one time quantum (or until it blocks/finishes).
7. Update the runnable set and repeat.

For process `i` with `t_i` tickets, its probability of winning a single draw is:

`P(process i wins) = t_i / T`

With repeated draws, the expected CPU share approaches the ticket share, assuming the processes remain runnable and use comparable time quanta. This is a statistical expectation, not a guarantee for a short interval.

## Example input and ticket shares

| Process | Tickets | Probability per draw | Ticket interval |
|---|---:|---:|---|
| P1 | 5 | 50% | 1–5 |
| P2 | 3 | 30% | 6–8 |
| P3 | 2 | 20% | 9–10 |
| **Total** | **10** | **100%** | |

If the random winning ticket is `7`, P2 wins because ticket 7 falls in the interval 6–8.

## Gantt chart — one possible execution

![Lottery Scheduling Gantt chart](assets/lottery_gantt_infographic.png)

The illustrative ten-slot schedule is:

```text
| P1 | P2 | P1 | P3 | P1 | P2 | P1 | P1 | P3 | P2 |
0    1    2    3    4    5    6    7    8    9   10
```

Each slot represents one time unit. The sequence is only one possible random outcome; it should not be interpreted as an exact 50/30/20 split in every ten draws.

## Animation

Open [`lottery_gantt_animation.mp4`](lottery_gantt_animation.mp4) to watch the ticket pool, winning ticket, selected process, and Gantt chart update over ten scheduling decisions. A GIF preview is also available at [`lottery_gantt_animation.gif`](lottery_gantt_animation.gif).

## Comparison: Lottery Scheduling vs. RM vs. EDF

| Property | Lottery Scheduling | Rate Monotonic (RM) | Earliest Deadline First (EDF) |
|---|---|---|---|
| Main objective | Probabilistic proportional CPU shares | Real-time scheduling of periodic tasks | Real-time scheduling by deadlines |
| Priority rule | Random draw weighted by tickets | Fixed priority; shorter task period gets higher priority | Dynamic priority; earliest absolute deadline first |
| Deterministic selection | No | Usually yes, with tie-breaking specified | Usually yes, with tie-breaking specified |
| CPU-share control | Directly adjusted through ticket counts | Not its primary objective | Not its primary objective |
| Deadline guarantees | None inherently | Schedulability depends on task assumptions and utilization | Can meet all deadlines under the classic uniprocessor preemptive model when assumptions hold and utilization is feasible |
| Strength | Flexible proportional-share allocation | Simple, predictable fixed-priority policy | Can use processor capacity efficiently under classic assumptions |
| Limitation | Short-term randomness; no inherent deadline guarantee | Can miss deadlines when task set is not schedulable; fixed priorities | Dynamic-priority overhead; guarantees depend on model assumptions |

**Important:** These algorithms target different goals. Lottery Scheduling is designed for proportional-share allocation, whereas RM and EDF are classic real-time scheduling policies. A fair comparison should use the same workload and explicitly measure both CPU-share error and deadline misses, rather than declaring one universally best.

## Advantages

- Simple selection mechanism.
- Flexible proportional allocation by changing ticket counts.
- Probabilistic fairness over many scheduling decisions.
- Can be extended with ticket transfer, ticket currencies, or compensation tickets.

## Limitations

- Random variation can create uneven short-term allocations.
- A process with tickets can still lose many consecutive lotteries.
- Ticket assignment strongly affects resource distribution.
- The basic algorithm does not guarantee deadlines or bounded response times.

## Basic pseudocode

```text
while there are runnable processes:
    total = sum(tickets[p] for p in runnable_processes)
    winner = random_integer(1, total)
    cumulative = 0

    for p in runnable_processes:
        cumulative += tickets[p]
        if cumulative >= winner:
            run(p, time_quantum)
            break

    update_runnable_processes()
```

## Complexity

With a simple linear scan over `n` runnable processes, selecting the winner takes `O(n)` time and `O(1)` auxiliary space. A tree of partial ticket sums can reduce selection to `O(log n)` for larger process sets.

## Repository and reproducibility

- Keep the source implementation as the source of truth for the actual algorithm behavior.
- If the implementation uses priorities to assign tickets, document that mapping and whether larger priority values mean more tickets.
- For reproducible results, allow a random seed to be set in tests.
- When evaluating performance, report the number of scheduling decisions, observed CPU share per process, absolute share error, context switches, and any deadline misses if deadlines are part of the workload.

## References

- Waldspurger and Weihl, *Lottery Scheduling: Flexible Proportional-Share Resource Management* (classic paper): https://www.usenix.org/legacy/publications/library/proceedings/osdi/full_papers/waldspurger.pdf
- Rate Monotonic and EDF are standard real-time scheduling policies; their guarantees depend on their scheduling model and task assumptions.
