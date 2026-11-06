"""Lottery Scheduling simulation with semaphore, monitor, or both."""
import argparse, random, threading
from dataclasses import dataclass
from pathlib import Path

GUARDS = ("semaphore", "monitor", "both")

@dataclass
class Process:
    pid: str
    burst: int
    tickets: int
    arrival: int = 0
    remaining: int = 0
    def __post_init__(self):
        if not self.pid.strip(): raise ValueError("Process ID must not be empty")
        if self.burst <= 0: raise ValueError("Burst time must be positive")
        if self.tickets <= 0: raise ValueError("Ticket count must be positive")
        if self.arrival < 0: raise ValueError("Arrival time cannot be negative")
        if self.remaining == 0: self.remaining = self.burst

@dataclass(frozen=True)
class Segment:
    pid: str
    start: int
    end: int
    tickets: int
    winning_ticket: int
    total_tickets: int

class CombinedGuard:
    def __init__(self, semaphore, condition):
        self.sem, self.cond = semaphore, condition
    def __enter__(self):
        self.sem.acquire()
        self.cond.acquire()
        return self
    def __exit__(self, *args):
        self.cond.release()
        self.sem.release()
        return False

class LotteryScheduler:
    def __init__(self, processes, mode="semaphore", quantum=2, seed=7):
        if mode not in GUARDS: raise ValueError(f"mode must be one of {GUARDS}")
        if quantum <= 0: raise ValueError("Quantum must be positive")
        items = [Process(p.pid, p.burst, p.tickets, p.arrival) for p in processes]
        ids = [p.pid for p in items]
        if len(ids) != len(set(ids)): raise ValueError("Process IDs must be unique")
        self.processes = {p.pid:p for p in items}
        self.mode, self.quantum = mode, quantum
        self.rng = random.Random(seed)
        self.semaphore = threading.Semaphore(1)
        self.condition = threading.Condition(threading.RLock())
        self.timeline, self.completion, self.draws = [], {}, []
    def _guard(self):
        if self.mode == "semaphore": return self.semaphore
        if self.mode == "monitor": return self.condition
        return CombinedGuard(self.semaphore, self.condition)
    def run(self):
        clock = 0
        while True:
            with self._guard():
                unfinished = [p for p in self.processes.values() if p.remaining > 0]
                if not unfinished: break
                ready = [p for p in unfinished if p.arrival <= clock]
                if not ready:
                    clock = min(p.arrival for p in unfinished)
                    ready = [p for p in unfinished if p.arrival <= clock]
                total = sum(p.tickets for p in ready)
                ticket = self.rng.randint(1, total)
                cursor, winner = 0, ready[-1]
                for p in ready:
                    cursor += p.tickets
                    if ticket <= cursor:
                        winner = p
                        break
                duration = min(self.quantum, winner.remaining)
                self.timeline.append(Segment(winner.pid, clock, clock+duration,
                                             winner.tickets, ticket, total))
                self.draws.append((clock, winner.pid, ticket, total))
                winner.remaining -= duration
                clock += duration
                if winner.remaining == 0: self.completion[winner.pid] = clock
                if self.mode in ("monitor", "both"): self.condition.notify_all()
        return list(self.timeline)
    def metrics(self):
        if any(p.remaining > 0 for p in self.processes.values()):
            raise RuntimeError("Call run() before metrics()")
        result = {}
        for pid,p in self.processes.items():
            c = self.completion[pid]; turnaround = c-p.arrival
            result[pid] = dict(tickets=p.tickets, burst=p.burst, arrival=p.arrival,
                               completion=c, turnaround=turnaround, waiting=turnaround-p.burst)
        return result

def example_processes():
    return [Process("P1",5,5), Process("P2",3,3), Process("P3",4,2),
            Process("P4",2,1,arrival=1), Process("P5",3,4,arrival=2)]

def render_gantt(timeline, output):
    output = Path(output); output.parent.mkdir(parents=True, exist_ok=True)
    end = timeline[-1].end if timeline else 1
    width, scale = max(700, 80+end*50), max(1, (max(700,80+end*50)-80)/end)
    colors = ["#8ecae6","#ffd166","#b7e4c7","#cdb4db","#ffadad"]
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="180">',
         '<rect width="100%" height="100%" fill="#f7faff"/>',
         '<text x="24" y="30" font-family="Arial" font-size="19" font-weight="bold">Lottery Scheduling — Gantt Chart</text>']
    for i,x in enumerate(timeline):
        left=40+x.start*scale; w=(x.end-x.start)*scale
        s += [f'<rect x="{left}" y="55" width="{w}" height="45" fill="{colors[i%len(colors)]}" stroke="#334155"/>',
              f'<text x="{left+w/2}" y="80" text-anchor="middle" font-family="Arial" font-size="12">{x.pid}</text>']
    s += ['</svg>']; output.write_text("\n".join(s), encoding="utf-8"); return output

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mode",choices=GUARDS,default="semaphore")
    ap.add_argument("--all",action="store_true")
    ap.add_argument("--quantum",type=int,default=2)
    ap.add_argument("--seed",type=int,default=7)
    ap.add_argument("--gantt",default="")
    a=ap.parse_args()
    for mode in (GUARDS if a.all else (a.mode,)):
        sch=LotteryScheduler(example_processes(),mode,a.quantum,a.seed); trace=sch.run()
        print(f"\\nMode: {mode} | quantum={a.quantum} | seed={a.seed}")
        print("Gantt: "+" | ".join(f"{x.start}-{x.end}:{x.pid}[ticket {x.winning_ticket}/{x.total_tickets}]" for x in trace))
        print("PID  Tickets  Burst  Completion  Waiting  Turnaround")
        for pid,m in sch.metrics().items():
            print(f"{pid:<4} {m['tickets']:<8} {m['burst']:<6} {m['completion']:<11} {m['waiting']:<8} {m['turnaround']}")
        if a.gantt:
            path=Path(a.gantt)
            if a.all: path=path.with_name(f"{path.stem}-{mode}{path.suffix or '.svg'}")
            render_gantt(trace,path); print(f"Gantt SVG written to: {path}")
if __name__=="__main__": main()
