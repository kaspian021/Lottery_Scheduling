"""Reproducible discrete-time Lottery Scheduling reference implementation.

This is an educational scheduler model, not a kernel scheduler. One draw grants
one quantum (or the remaining burst when shorter) to the selected runnable job.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from random import Random
from typing import Iterable, Mapping
import math


@dataclass(frozen=True)
class Task:
    pid: str
    tickets: int
    burst: int
    arrival: int = 0
    deadline: int | None = None
    period: int | None = None

    def __post_init__(self):
        if not self.pid or not isinstance(self.pid, str):
            raise ValueError("pid must be a non-empty string")
        if isinstance(self.tickets, bool) or not isinstance(self.tickets, int) or self.tickets <= 0:
            raise ValueError("tickets must be a positive integer")
        if isinstance(self.burst, bool) or not isinstance(self.burst, int) or self.burst <= 0:
            raise ValueError("burst must be a positive integer")
        if isinstance(self.arrival, bool) or not isinstance(self.arrival, int) or self.arrival < 0:
            raise ValueError("arrival must be a non-negative integer")
        if self.deadline is not None and self.deadline < self.arrival:
            raise ValueError("deadline cannot be earlier than arrival")
        if self.period is not None and self.period <= 0:
            raise ValueError("period must be positive")


@dataclass
class Slice:
    start: int
    end: int
    pid: str
    draw: int | None = None
    total_tickets: int | None = None
    interval_low: int | None = None
    interval_high: int | None = None


@dataclass
class ScheduleResult:
    policy: str
    seed: int | None
    quantum: int
    events: list[Slice]
    metrics: dict[str, dict]
    total_time: int
    busy_time: int

    def to_dict(self):
        return {
            "policy": self.policy,
            "seed": self.seed,
            "quantum": self.quantum,
            "events": [asdict(e) for e in self.events],
            "metrics": self.metrics,
            "total_time": self.total_time,
            "busy_time": self.busy_time,
        }


def _validate_tasks(tasks: Iterable[Task]):
    tasks = list(tasks)
    if not tasks:
        raise ValueError("at least one task is required")
    ids = [t.pid for t in tasks]
    if len(ids) != len(set(ids)):
        raise ValueError("task identifiers must be unique")
    if not all(isinstance(t, Task) for t in tasks):
        raise TypeError("tasks must contain Task instances")
    return tasks


def draw_lottery(ticket_map: Mapping[str, int], rounds: int, seed: int | None = None):
    """Return one record per draw for a fixed, always-runnable ticket pool."""
    if not ticket_map:
        raise ValueError("ticket_map cannot be empty")
    if isinstance(rounds, bool) or not isinstance(rounds, int) or rounds < 1:
        raise ValueError("rounds must be a positive integer")
    items = list(ticket_map.items())
    for name, tickets in items:
        if not name or isinstance(tickets, bool) or not isinstance(tickets, int) or tickets <= 0:
            raise ValueError("each process needs a name and a positive integer ticket count")
    total = sum(t for _, t in items)
    rng = Random(seed)
    records = []
    for decision in range(1, rounds + 1):
        draw = rng.randint(1, total)
        cumulative = 0
        for name, tickets in items:
            low = cumulative + 1
            cumulative += tickets
            if draw <= cumulative:
                records.append({
                    "decision": decision, "draw": draw, "total_tickets": total,
                    "winner": name, "interval_low": low, "interval_high": cumulative,
                })
                break
    return records


def share_summary(ticket_map: Mapping[str, int], records: list[dict]):
    total_tickets = sum(ticket_map.values())
    rounds = len(records)
    counts = {name: 0 for name in ticket_map}
    for record in records:
        counts[record["winner"]] += 1
    result = {}
    for name, tickets in ticket_map.items():
        expected = tickets / total_tickets
        observed = counts[name] / rounds if rounds else 0.0
        standard_error = math.sqrt(expected * (1 - expected) / rounds) if rounds else 0.0
        result[name] = {
            "tickets": tickets,
            "expected_share": expected,
            "wins": counts[name],
            "observed_share": observed,
            "absolute_error": abs(observed - expected),
            "binomial_standard_error": standard_error,
        }
    return result


def _metrics(tasks: list[Task], first_start: dict[str, int], finish: dict[str, int], executed: dict[str, int]):
    out = {}
    for task in tasks:
        end = finish[task.pid]
        start = first_start[task.pid]
        turnaround = end - task.arrival
        out[task.pid] = {
            "arrival": task.arrival,
            "burst": task.burst,
            "tickets": task.tickets,
            "first_start": start,
            "finish": end,
            "response": start - task.arrival,
            "turnaround": turnaround,
            "waiting": turnaround - task.burst,
            "cpu_time": executed[task.pid],
            "deadline": task.deadline,
            "deadline_missed": task.deadline is not None and end > task.deadline,
        }
    return out


def run_lottery(tasks: Iterable[Task], quantum: int = 1, seed: int | None = 0) -> ScheduleResult:
    """Run finite CPU bursts using weighted random draws among runnable jobs."""
    tasks = _validate_tasks(tasks)
    if isinstance(quantum, bool) or not isinstance(quantum, int) or quantum < 1:
        raise ValueError("quantum must be a positive integer")
    rng = Random(seed)
    remaining = {t.pid: t.burst for t in tasks}
    task_by_id = {t.pid: t for t in tasks}
    first_start: dict[str, int] = {}
    finish: dict[str, int] = {}
    executed = {t.pid: 0 for t in tasks}
    events: list[Slice] = []
    now = 0
    while len(finish) < len(tasks):
        ready = [t for t in tasks if t.arrival <= now and remaining[t.pid] > 0]
        if not ready:
            next_arrival = min(t.arrival for t in tasks if remaining[t.pid] > 0)
            if next_arrival <= now:
                raise RuntimeError("scheduler made no progress")
            events.append(Slice(now, next_arrival, "IDLE"))
            now = next_arrival
            continue
        total = sum(t.tickets for t in ready)
        draw = rng.randint(1, total)
        cumulative = 0
        winner = None
        low = high = None
        for task in ready:
            ticket_low = cumulative + 1
            cumulative += task.tickets
            if draw <= cumulative:
                winner, low, high = task, ticket_low, cumulative
                break
        if winner is None:
            raise RuntimeError("ticket interval selection failed")
        pid = winner.pid
        duration = min(quantum, remaining[pid])
        start, end = now, now + duration
        first_start.setdefault(pid, start)
        remaining[pid] -= duration
        executed[pid] += duration
        events.append(Slice(start, end, pid, draw, total, low, high))
        now = end
        if remaining[pid] == 0:
            finish[pid] = now
    busy = sum(e.end - e.start for e in events if e.pid != "IDLE")
    return ScheduleResult("LOTTERY", seed, quantum, events,
                          _metrics(tasks, first_start, finish, executed), now, busy)


def run_priority(tasks: Iterable[Task], policy: str = "EDF") -> ScheduleResult:
    """Unit-tick preemptive EDF/RM reference for comparable single-job workloads."""
    tasks = _validate_tasks(tasks)
    policy = policy.upper()
    if policy not in {"EDF", "RM"}:
        raise ValueError("policy must be EDF or RM")
    if any(not isinstance(x, int) for t in tasks for x in (t.arrival, t.burst)):
        raise ValueError("this reference model uses integer arrival and burst times")
    if policy == "EDF" and any(t.deadline is None for t in tasks):
        raise ValueError("EDF requires a deadline for every task")
    if policy == "RM" and any(t.period is None for t in tasks):
        raise ValueError("RM requires a period for every task")
    remaining = {t.pid: t.burst for t in tasks}
    first_start: dict[str, int] = {}
    finish: dict[str, int] = {}
    executed = {t.pid: 0 for t in tasks}
    events: list[Slice] = []
    now = 0
    while len(finish) < len(tasks):
        ready = [t for t in tasks if t.arrival <= now and remaining[t.pid] > 0]
        if not ready:
            next_arrival = min(t.arrival for t in tasks if remaining[t.pid] > 0)
            events.append(Slice(now, next_arrival, "IDLE"))
            now = next_arrival
            continue
        if policy == "EDF":
            winner = min(ready, key=lambda t: (t.deadline, t.arrival, t.pid))
        else:
            winner = min(ready, key=lambda t: (t.period, t.arrival, t.pid))
        pid = winner.pid
        first_start.setdefault(pid, now)
        remaining[pid] -= 1
        executed[pid] += 1
        if events and events[-1].pid == pid and events[-1].end == now:
            events[-1].end += 1
        else:
            events.append(Slice(now, now + 1, pid))
        now += 1
        if remaining[pid] == 0:
            finish[pid] = now
    busy = sum(e.end - e.start for e in events if e.pid != "IDLE")
    return ScheduleResult(policy, None, 1, events,
                          _metrics(tasks, first_start, finish, executed), now, busy)


def concurrent_draws(ticket_map: Mapping[str, int], workers: int = 4,
                     draws_per_worker: int = 250, seed: int = 0,
                     primitive: str = "semaphore"):
    """Protect a shared lottery pool using a semaphore or a monitor condition."""
    from threading import Thread, Semaphore, Condition
    if workers < 1 or draws_per_worker < 1:
        raise ValueError("workers and draws_per_worker must be positive")
    if not ticket_map or any(not isinstance(v, int) or v <= 0 for v in ticket_map.values()):
        raise ValueError("ticket_map must contain positive integer ticket counts")
    primitive = primitive.lower()
    if primitive not in {"semaphore", "monitor", "lock"}:
        raise ValueError("primitive must be semaphore, monitor, or lock")
    names = list(ticket_map)
    weights = [ticket_map[n] for n in names]
    total = sum(weights)
    rng = Random(seed)
    counts = {n: 0 for n in names}
    trace = []
    if primitive == "semaphore":
        guard = Semaphore(1)
        def critical():
            draw = rng.randint(1, total)
            cumulative = 0
            winner = None
            for name, weight in zip(names, weights):
                cumulative += weight
                if draw <= cumulative:
                    winner = name; break
            counts[winner] += 1
            trace.append(winner)
    else:
        cv = Condition()
        def critical():
            with cv:
                draw = rng.randint(1, total)
                cumulative = 0
                winner = None
                for name, weight in zip(names, weights):
                    cumulative += weight
                    if draw <= cumulative:
                        winner = name; break
                counts[winner] += 1
                trace.append(winner)
                cv.notify_all()
        guard = None
    def worker():
        for _ in range(draws_per_worker):
            if primitive == "semaphore":
                with guard:
                    critical()
            else:
                critical()
    threads = [Thread(target=worker) for _ in range(workers)]
    for thread in threads: thread.start()
    for thread in threads: thread.join()
    return {"primitive": primitive, "workers": workers,
            "draws_per_worker": draws_per_worker,
            "total_draws": sum(counts.values()), "counts": counts,
            "trace": trace}


def simulate_rw_phases(requests: list[dict], seed: int = 0, policy: str = "lottery"):
    """A phase-based readers/writers model with exclusive writer phases.

    A reader phase admits the readers currently waiting as one cohort. A writer
    phase admits one writer. Lottery chooses a phase in proportion to the sum
    of waiting tickets; reader-/writer-preference policies are baselines.
    """
    policy = policy.lower()
    if policy not in {"lottery", "reader_preference", "writer_preference"}:
        raise ValueError("unknown readers-writers policy")
    pending = [dict(r) for r in requests]
    for r in pending:
        if r.get("kind") not in {"reader", "writer"} or int(r.get("tickets", 0)) <= 0:
            raise ValueError("requests need kind=reader/writer and positive tickets")
    rng = Random(seed)
    trace, served = [], []
    turn = 0
    while pending:
        readers = [r for r in pending if r["kind"] == "reader"]
        writers = [r for r in pending if r["kind"] == "writer"]
        if policy == "reader_preference":
            phase_kind = "reader" if readers else "writer"
        elif policy == "writer_preference":
            phase_kind = "writer" if writers else "reader"
        else:
            rt, wt = sum(r["tickets"] for r in readers), sum(r["tickets"] for r in writers)
            draw = rng.randint(1, rt + wt)
            phase_kind = "reader" if draw <= rt else "writer"
        if phase_kind == "reader":
            cohort = [r for r in pending if r["kind"] == "reader"]
        else:
            pool = [r for r in pending if r["kind"] == "writer"]
            total = sum(r["tickets"] for r in pool)
            draw = rng.randint(1, total)
            acc = 0; chosen = None
            for r in pool:
                acc += r["tickets"]
                if draw <= acc: chosen = r; break
            cohort = [chosen]
        if not cohort:
            raise RuntimeError("empty phase")
        turn += 1
        for r in cohort:
            pending.remove(r)
            trace.append({"phase": turn, "kind": phase_kind, "request": r["id"],
                          "tickets": r["tickets"], "members_in_phase": [x["id"] for x in cohort]})
            served.append(r["id"])
    return {"policy": policy, "trace": trace, "served_order": served,
            "all_served": len(served) == len(requests),
            "phases": turn}


def simulate_dining(n: int = 5, meals_each: int = 2, tickets: list[int] | None = None,
                    seed: int = 0, eat_ticks: int = 2, age_boost: int = 0):
    """Discrete-event Dining Philosophers demo using lottery among eligible eaters.

    A meal starts only when both adjacent forks are free and fewer than N-1
    philosophers occupy the room. The pair of forks is reserved atomically,
    which models an ordered/atomic acquisition protocol and avoids hold-and-wait.
    Ticket aging increases a waiter's weight but is not a hard starvation bound.
    """
    if n < 3 or meals_each < 1 or eat_ticks < 1 or age_boost < 0:
        raise ValueError("n>=3, meals_each>=1, eat_ticks>=1, age_boost>=0 required")
    tickets = list(tickets or [1] * n)
    if len(tickets) != n or any(not isinstance(t, int) or t <= 0 for t in tickets):
        raise ValueError("one positive ticket count is required per philosopher")
    rng = Random(seed)
    completed = [0] * n
    waiting_age = [0] * n
    active: dict[int, int] = {}  # philosopher -> finish time
    trace = []
    now = 0
    seq = 0
    while sum(completed) < n * meals_each:
        for p, end in list(active.items()):
            if end <= now:
                seq += 1; trace.append({"seq":seq,"time":now,"philosopher":p,"action":"finish"})
                del active[p]
                completed[p] += 1
        if sum(completed) >= n * meals_each:
            break
        occupied = set()
        for p in active:
            occupied.add(p); occupied.add((p + 1) % n)
        eligible = [p for p in range(n)
                    if completed[p] < meals_each and p not in active
                    and p not in occupied and (p + 1) % n not in occupied
                    and len(active) < n - 1]
        if eligible:
            weights = {p: tickets[p] + waiting_age[p] * age_boost for p in eligible}
            total = sum(weights.values())
            draw = rng.randint(1, total)
            acc = 0; winner = None
            for p in eligible:
                acc += weights[p]
                if draw <= acc: winner = p; break
            for p in range(n):
                if p != winner and completed[p] < meals_each and p not in active:
                    waiting_age[p] += 1
            seq += 1
            trace.append({"seq":seq,"time":now,"philosopher":winner,"action":"eat_start",
                          "forks":[winner,(winner+1)%n],"draw":draw,
                          "total_tickets":total,"effective_tickets":weights[winner]})
            active[winner] = now + eat_ticks
            continue
        if active:
            now = min(active.values())
        else:
            raise RuntimeError("no eligible philosopher and no active eater: deadlock")
    return {"philosophers":n,"meals_each":meals_each,"meals_completed":sum(completed),
            "per_philosopher":completed,"finish_time":now,"trace":trace,
            "all_completed":completed == [meals_each]*n,
            "starvation_guarantee":"none; lottery plus optional aging is probabilistic"}
