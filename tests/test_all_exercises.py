from shared.experiments import RUNNERS

def test_all_exercises_have_runnable_experiment():
    assert sorted(RUNNERS) == list(range(1,9))
    for number, runner in RUNNERS.items():
        result = runner()
        assert result["exercise"] == number
        assert result["topic"]
