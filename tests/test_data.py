import pytest

from mlp9x9.data import flatten_image, validate_flat_input


def test_flatten_image_9x9_zeros_length_81():
    image = [[0 for _ in range(9)] for _ in range(9)]
    flat = flatten_image(image)
    assert isinstance(flat, list)
    assert len(flat) == 81


def test_validate_flat_input_raises_on_incorrect_length():
    with pytest.raises(ValueError):
        validate_flat_input([0.0] * 80)
