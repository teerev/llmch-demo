from __future__ import annotations

from .cli import main


def _entry() -> None:
    raise SystemExit(main())


if __name__ == "__main__":
    _entry()
