from shared.experiments import run_exercise


def test_exercise_7_returns_expected_record():
    result = run_exercise(7)
    assert result["exercise"] == 7
    assert "topic" in result
