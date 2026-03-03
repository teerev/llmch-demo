from __future__ import annotations

import argparse
import time
from typing import List, Optional


def build_output(iterations: int) -> list[str]:
    # Deterministic placeholder output; iterations is accepted for future expansion.
    return ["Pretending to work hard...", "All tasks complete."]


def run(args: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="pretend_productivity")
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--no-sleep", action="store_true")
    ns = parser.parse_args(args)

    lines = build_output(ns.iterations)
    for i, line in enumerate(lines):
        print(line)
        if not ns.no_sleep and i != len(lines) - 1:
            time.sleep(0.1)

    return 0
