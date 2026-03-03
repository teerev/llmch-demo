from __future__ import annotations

from dia_mujer.info import get_summary
from dia_mujer.__main__ import main


def test_get_summary_contains_colombia() -> None:
    summary = get_summary()
    assert isinstance(summary, str)
    assert "Colombia" in summary


def test_cli_main_prints_colombia(capsys) -> None:
    main()
    captured = capsys.readouterr()
    assert "Colombia" in captured.out
