"""Package entrypoint for `python -m ascii_art`.

Delegates to :func:`ascii_art.cli.main`.
"""

from __future__ import annotations

from . import cli


def _run() -> None:
    raise SystemExit(cli.main())


if __name__ == "__main__":
    _run()
