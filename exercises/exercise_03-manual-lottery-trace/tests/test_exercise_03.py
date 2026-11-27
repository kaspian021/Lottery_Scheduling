from shared.experiments import run_exercise


def test_exercise_3_returns_expected_record():
    result = run_exercise(3)
    assert result["exercise"] == 3
    assert "topic" in result


def test_manual_trace_csv_has_all_seeded_draws():
    from pathlib import Path
    import csv
    root = Path(__file__).resolve().parents[3]
    path = root / "exercises/exercise_03-manual-lottery-trace/outputs/manual_draws.csv"
    with path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 15
    assert all(int(row["interval_low"]) <= int(row["draw"]) <= int(row["interval_high"]) for row in rows)
