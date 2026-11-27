from shared.experiments import run_exercise


def test_exercise_5_returns_expected_record():
    result = run_exercise(5)
    assert result["exercise"] == 5
    assert "topic" in result
