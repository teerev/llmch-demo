from __future__ import annotations

import argparse
import json
from typing import Sequence

from quadrl.config import TrainConfig
from quadrl.trainer import train


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="quadrl", description="Run QuadRL training.")
    parser.add_argument("--steps", type=int, default=None, help="Total environment steps to run.")
    parser.add_argument(
        "--max-episode-steps",
        type=int,
        default=None,
        help="Maximum steps per episode before termination.",
    )
    parser.add_argument("--seed", type=int, default=None, help="Random seed.")
    parser.add_argument(
        "--target-distance",
        type=float,
        default=None,
        help="Target distance for episode completion.",
    )
    parser.add_argument(
        "--log-interval",
        type=int,
        default=None,
        help="Logging interval in steps.",
    )

    args = parser.parse_args(argv)

    config = TrainConfig(
        total_steps=args.steps if args.steps is not None else TrainConfig.total_steps,
        max_episode_steps=(
            args.max_episode_steps
            if args.max_episode_steps is not None
            else TrainConfig.max_episode_steps
        ),
        seed=args.seed if args.seed is not None else TrainConfig.seed,
        target_distance=(
            args.target_distance
            if args.target_distance is not None
            else TrainConfig.target_distance
        ),
        log_interval=(
            args.log_interval if args.log_interval is not None else TrainConfig.log_interval
        ),
    )

    stats = train(config)
    print(json.dumps(stats))


if __name__ == "__main__":
    main()
