from __future__ import annotations
from .lottery_scheduler import Task, draw_lottery, share_summary, run_lottery, run_priority, concurrent_draws, simulate_rw_phases, simulate_dining
import json

TICKETS={"P1":5,"P2":3,"P3":2}


def ex1():
    records=draw_lottery(TICKETS,10000,seed=20261127)
    return {"exercise":1,"topic":"Lottery Scheduling introduction",
            "ticket_pool":TICKETS,"decisions":len(records),
            "shares":share_summary(TICKETS,records),"sample_trace":records[:25]}


def ex2():
    tasks=[Task("P1",tickets=5,burst=4,arrival=0,deadline=7,period=5),
           Task("P2",tickets=3,burst=3,arrival=0,deadline=5,period=7),
           Task("P3",tickets=2,burst=2,arrival=1,deadline=8,period=9)]
    results={"LOTTERY":run_lottery(tasks,quantum=1,seed=42).to_dict(),
             "EDF":run_priority(tasks,"EDF").to_dict(),
             "RM":run_priority(tasks,"RM").to_dict()}
    return {"exercise":2,"topic":"Lottery vs EDF and RM", "workload":[t.__dict__ for t in tasks],"results":results,
            "interpretation":"Lottery optimizes proportional shares, EDF/RM prioritize deadline-related order; these objectives are not interchangeable."}


def ex3():
    records=draw_lottery(TICKETS,15,seed=7)
    return {"exercise":3,"topic":"Hand-worked ticket draws", "ticket_pool":TICKETS,
            "intervals":{"P1":"1-5","P2":"6-8","P3":"9-10"},"draws":records,
            "counts":share_summary(TICKETS,records)}


def ex4():
    runs={p:concurrent_draws(TICKETS,workers=4,draws_per_worker=500,seed=19,primitive=p)
          for p in ("semaphore","monitor")}
    return {"exercise":4,"topic":"Synchronization and protected lottery state", "runs":runs,
            "note":"The critical section protects the PRNG draw and shared counters. This demonstrates Semaphore/Condition protection, not a kernel scheduler."}


def ex5():
    sem=concurrent_draws({"CPU":5,"IO":3,"LOCK":2},workers=3,draws_per_worker=100,seed=5,primitive="semaphore")
    mon=concurrent_draws({"CPU":5,"IO":3,"LOCK":2},workers=3,draws_per_worker=100,seed=5,primitive="monitor")
    return {"exercise":5,"topic":"Lottery scheduler with semaphore/monitor", "semaphore":sem,"monitor":mon,
            "same_total":sem["total_draws"]==mon["total_draws"]==300,
            "note":"Concurrent interleavings may alter the observed draw order; only totals and protected-state invariants are deterministic."}


def ex6():
    records=draw_lottery(TICKETS,5000,seed=2026)
    return {"exercise":6,"topic":"Research and seminar data", "reference":"Waldspurger & Weihl, OSDI 1994",
            "ticket_pool":TICKETS,"decisions":5000,"shares":share_summary(TICKETS,records),
            "research_claim":"Lottery scheduling provides randomized proportional-share control; short-run outcomes vary and hard deadline guarantees do not follow from ticket weights."}


def ex7():
    req=[{"id":"R1","kind":"reader","tickets":3},{"id":"R2","kind":"reader","tickets":2},
         {"id":"W1","kind":"writer","tickets":5},{"id":"R3","kind":"reader","tickets":4},
         {"id":"W2","kind":"writer","tickets":2},{"id":"R4","kind":"reader","tickets":1}]
    runs={p:simulate_rw_phases(req,seed=31,policy=p) for p in ("reader_preference","writer_preference","lottery")}
    return {"exercise":7,"topic":"Readers-writers fairness", "requests":req,"runs":runs,
            "safety":"A writer phase is exclusive; a reader phase admits only a reader cohort.",
            "fairness_limit":"Lottery improves proportional arbitration but does not give a deterministic waiting-time bound."}


def ex8():
    result=simulate_dining(n=5,meals_each=3,tickets=[5,4,3,2,1],seed=2026,eat_ticks=2,age_boost=2)
    return {"exercise":8,"topic":"Dining philosophers and starvation", **result,
            "deadlock_control":"At most N-1 philosophers may enter; each pair of forks is reserved atomically, equivalent to an ordered resource-acquisition discipline.",
            "starvation_control":"Ticket aging increases selection probability with waiting, but remains probabilistic and is not a strict bounded-wait guarantee."}


RUNNERS={1:ex1,2:ex2,3:ex3,4:ex4,5:ex5,6:ex6,7:ex7,8:ex8}

def run_exercise(number):
    if number not in RUNNERS: raise ValueError("exercise number must be 1..8")
    return RUNNERS[number]()
