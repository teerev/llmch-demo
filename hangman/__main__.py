from __future__ import annotations

import sys

from . import cli


def _run() -> int:
    return cli.main()


if __name__ == "__main__":
    raise SystemExit(_run())
