import pytest
from shared.lottery_scheduler import Task, draw_lottery, share_summary, run_lottery, run_priority, concurrent_draws, simulate_rw_phases, simulate_dining


def test_ticket_intervals_and_deterministic_draws():
    a = draw_lottery({"P1":5,"P2":3,"P3":2}, 100, seed=4)
    b = draw_lottery({"P1":5,"P2":3,"P3":2}, 100, seed=4)
    assert a == b
    assert all(1 <= x["draw"] <= 10 for x in a)
    assert all(x["interval_low"] <= x["draw"] <= x["interval_high"] for x in a)


def test_share_summary_sums_to_one():
    m={"A":4,"B":1}; rows=draw_lottery(m,2000,seed=9); s=share_summary(m,rows)
    assert abs(sum(x["observed_share"] for x in s.values())-1) < 1e-12
    assert abs(s["A"]["observed_share"]-.8) < .05


def test_lottery_completion_and_metrics():
    tasks=[Task("A",5,3,0),Task("B",2,2,1)]
    r=run_lottery(tasks,quantum=1,seed=5)
    assert set(r.metrics)=={"A","B"}
    assert all(v["cpu_time"]==v["burst"] for v in r.metrics.values())
    assert r.busy_time==5


def test_priority_schedulers_require_parameters():
    tasks=[Task("A",2,2,deadline=5,period=3)]
    assert run_priority(tasks,"EDF").policy=="EDF"
    assert run_priority(tasks,"RM").policy=="RM"
    with pytest.raises(ValueError): run_priority([Task("B",1,1)],"EDF")


def test_task_validation():
    with pytest.raises(ValueError): Task("A",0,1)
    with pytest.raises(ValueError): Task("A",1,0)
    with pytest.raises(ValueError): run_lottery([Task("A",1,1),Task("A",1,2)])


def test_concurrent_draws_preserve_counter_invariant():
    for primitive in ("semaphore","monitor"):
        result=concurrent_draws({"A":2,"B":1},workers=4,draws_per_worker=100,seed=7,primitive=primitive)
        assert result["total_draws"]==400
        assert sum(result["counts"].values())==400


def test_readers_writers_exclusive_phase_model():
    req=[{"id":"R1","kind":"reader","tickets":2},{"id":"W1","kind":"writer","tickets":3},{"id":"R2","kind":"reader","tickets":1}]
    for policy in ("reader_preference","writer_preference","lottery"):
        result=simulate_rw_phases(req,seed=4,policy=policy)
        assert result["all_served"]
        assert len(result["served_order"])==3


def test_dining_finishes_and_no_adjacent_meals_start_together():
    r=simulate_dining(5,2,[5,4,3,2,1],seed=12,eat_ticks=2,age_boost=2)
    assert r["all_completed"]
    active=set()
    for e in r["trace"]:
        p=e["philosopher"]
        if e["action"]=="eat_start":
            assert p not in active and (p+1)%5 not in active and (p-1)%5 not in active
            active.add(p)
        else:
            active.remove(p)


def test_bad_draw_inputs_rejected():
    with pytest.raises(ValueError): draw_lottery({},1)
    with pytest.raises(ValueError): draw_lottery({"A":1},0)
