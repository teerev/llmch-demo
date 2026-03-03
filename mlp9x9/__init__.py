__version__ = '0.1.0'

from .model import MLP
from .data import flatten_image, validate_flat_input

__all__ = [
    'MLP',
    'flatten_image',
    'validate_flat_input',
]
