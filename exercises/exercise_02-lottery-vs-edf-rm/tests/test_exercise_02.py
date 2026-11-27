from shared.experiments import run_exercise


def test_exercise_2_returns_expected_record():
    result = run_exercise(2)
    assert result["exercise"] == 2
    assert "topic" in result
