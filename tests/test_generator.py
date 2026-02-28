from countdown.generator import generate_numbers


class StubRNG:
    def __init__(self, sequence):
        self._sequence = list(sequence)
        self._i = 0

    def randint(self, a, b):
        value = self._sequence[self._i]
        self._i += 1
        return value


def test_generate_numbers_deterministic_stub_rng():
    rng = StubRNG([3, 4, 5, 123])
    result = generate_numbers(
        count=3,
        min_value=1,
        max_value=10,
        target_min=100,
        target_max=999,
        rng=rng,
    )
    assert result == {"numbers": [3, 4, 5], "target": 123}
