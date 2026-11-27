from shared.experiments import run_exercise


def test_exercise_6_returns_expected_record():
    result = run_exercise(6)
    assert result["exercise"] == 6
    assert "topic" in result
