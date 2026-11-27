from shared.experiments import run_exercise


def test_exercise_4_returns_expected_record():
    result = run_exercise(4)
    assert result["exercise"] == 4
    assert "topic" in result
