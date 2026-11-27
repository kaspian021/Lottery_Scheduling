from shared.experiments import run_exercise


def test_exercise_1_returns_expected_record():
    result = run_exercise(1)
    assert result["exercise"] == 1
    assert "topic" in result
