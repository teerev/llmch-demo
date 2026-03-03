import json
import os
from typing import Any

from .models import LightState


DEFAULT_STATE_PATH = os.path.join("data", "state.json")


def get_state_path() -> str:
    return os.environ.get("LIGHTS_STATE_PATH", DEFAULT_STATE_PATH)


def _validate_state_payload(payload: Any) -> LightState:
    if not isinstance(payload, dict):
        raise ValueError("State JSON must be an object")
    if "on" not in payload:
        raise ValueError("State JSON must contain key 'on'")
    if not isinstance(payload["on"], bool):
        raise ValueError("State JSON key 'on' must be a boolean")
    return LightState(on=payload["on"])


def load_state(path: str) -> LightState:
    if not os.path.exists(path):
        return LightState(on=False)

    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    return _validate_state_payload(payload)


def save_state(path: str, state: LightState) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump({"on": state.on}, f)
