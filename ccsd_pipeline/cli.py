from __future__ import annotations

import argparse
from typing import Sequence

from ccsd_pipeline.schema import load_config
from ccsd_pipeline.training import train_model


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ccsd_pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)

    train_p = subparsers.add_parser("train", help="Train a model from a JSON config")
    train_p.add_argument(
        "--config",
        required=True,
        metavar="PATH",
        help="Path to JSON training config",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "train":
        config = load_config(args.config)
        result = train_model(config)
        print(result.model_path)
        return 0

    # Should be unreachable due to required subparser.
    parser.error(f"Unknown command: {args.command}")
    return 2
