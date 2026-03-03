from __future__ import annotations

from lights_app.controller import get_state, turn_off, turn_on


def test_get_state_defaults_to_off_when_file_missing(tmp_path):
    state_path = tmp_path / "state.json"
    state = get_state(str(state_path))
    assert state.on is False


def test_turn_on_saves_and_get_state_reads(tmp_path):
    state_path = tmp_path / "state.json"

    state_on = turn_on(str(state_path))
    assert state_on.on is True

    state_read = get_state(str(state_path))
    assert state_read.on is True


def test_turn_off_saves_and_get_state_reads(tmp_path):
    state_path = tmp_path / "state.json"

    turn_on(str(state_path))
    state_off = turn_off(str(state_path))
    assert state_off.on is False

    state_read = get_state(str(state_path))
    assert state_read.on is False
