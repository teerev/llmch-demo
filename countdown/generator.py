import random


def generate_numbers(
    count=6,
    min_value=1,
    max_value=10,
    target_min=100,
    target_max=999,
    rng=None,
):
    """Generate a Countdown numbers round.

    Contract is frozen by work order; implementation to be provided later.
    """
    if rng is None:
        rng = random.Random()

    numbers = [rng.randint(min_value, max_value) for _ in range(count)]
    target = rng.randint(target_min, target_max)

    return {"numbers": numbers, "target": target}
