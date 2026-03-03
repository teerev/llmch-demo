from __future__ import annotations

from .models import LightState
from .storage import get_state_path, load_state, save_state


def _resolve_path(path: str | None) -> str:
    return get_state_path() if path is None else path


def get_state(path: str | None = None) -> LightState:
    """Load and return the current light state."""
    return load_state(_resolve_path(path))


def turn_on(path: str | None = None) -> LightState:
    """Set the light state to on, persist it, and return it."""
    resolved = _resolve_path(path)
    state = LightState(on=True)
    save_state(resolved, state)
    return state


def turn_off(path: str | None = None) -> LightState:
    """Set the light state to off, persist it, and return it."""
    resolved = _resolve_path(path)
    state = LightState(on=False)
    save_state(resolved, state)
    return state
