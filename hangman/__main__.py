from __future__ import annotations

import sys

from . import cli


def main() -> None:
    raise SystemExit(cli.main())


if __name__ == "__main__":
    main()
