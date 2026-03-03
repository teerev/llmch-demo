from __future__ import annotations

import argparse
from typing import Sequence

from .controller import get_state, turn_off, turn_on


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="lights_app")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Print current light status")
    subparsers.add_parser("on", help="Turn the light on")
    subparsers.add_parser("off", help="Turn the light off")

    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint.

    Commands:
      - status: print current state ('on' or 'off')
      - on: set state to on and print 'on'
      - off: set state to off and print 'off'

    Returns 0 on success.
    """
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "status":
        state = get_state()
        print("on" if state.on else "off")
        return 0

    if args.command == "on":
        turn_on()
        print("on")
        return 0

    if args.command == "off":
        turn_off()
        print("off")
        return 0

    # Should be unreachable due to required subcommand.
    parser.error("missing command")
    return 2
