from shared.experiments import run_exercise


def test_exercise_8_returns_expected_record():
    result = run_exercise(8)
    assert result["exercise"] == 8
    assert "topic" in result
