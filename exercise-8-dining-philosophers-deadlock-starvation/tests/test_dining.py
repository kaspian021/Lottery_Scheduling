import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))

from dining import (
    FairDiningMonitor,
    detect_deadlock_cycle,
    run_fair_monitor,
    run_resource_hierarchy,
)


def test_constructed_circular_wait_is_detected_and_cleaned_up():
    result = detect_deadlock_cycle(count=5, timeout=0.03)
    assert result["deadlock_witness"] is True
    assert all(not row["acquired_right_fork"] for row in result["outcomes"])


def test_global_fork_order_completes_without_deadlock():
    result = run_resource_hierarchy(count=5, meals=8)
    assert result["all_meals_completed"] is True
    assert result["completed_meals"] == [8] * 5


def test_fair_monitor_preserves_nonconflicting_concurrency_and_safety():
    result = run_fair_monitor(count=5, meals=8)
    assert result["all_meals_completed"] is True
    assert result["mutual_exclusion_verified"] is True
    assert result["max_simultaneous_eaters"] <= 2
    assert len(result["entry_log"]) == 40


def test_monitor_rejects_invalid_philosopher():
    monitor = FairDiningMonitor(5)
    try:
        monitor.acquire(5)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid index must be rejected")
