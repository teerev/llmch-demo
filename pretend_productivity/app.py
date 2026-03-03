from __future__ import annotations

import argparse
import time
from typing import Optional


def build_output(iterations: int) -> list[str]:
    lines: list[str] = ["Pretending to work hard..."]
    for i in range(1, iterations + 1):
        lines.append(f"[INFO] Starting task {i}")
        lines.append("Progress: [#####-----] 50%")
        lines.append("CPU Usage: 99%")
    lines.append("All tasks complete.")
    return lines


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
