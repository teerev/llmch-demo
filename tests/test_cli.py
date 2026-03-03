from __future__ import annotations

from pathlib import Path

from lights_app.cli import main


def test_cli_status_on_off(tmp_path, monkeypatch, capsys):
    state_path = tmp_path / "state.json"
    monkeypatch.setenv("LIGHTS_STATE_PATH", str(state_path))

    # Default state should be off when no state file exists.
    rc = main(["status"])
    assert rc == 0
    out = capsys.readouterr().out
    assert out == "off\n"

    rc = main(["on"])
    assert rc == 0
    out = capsys.readouterr().out
    assert out == "on\n"

    rc = main(["status"])
    assert rc == 0
    out = capsys.readouterr().out
    assert out == "on\n"

    rc = main(["off"])
    assert rc == 0
    out = capsys.readouterr().out
    assert out == "off\n"

    rc = main(["status"])
    assert rc == 0
    out = capsys.readouterr().out
    assert out == "off\n"
