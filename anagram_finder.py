"""Anagram finder core logic.

This module can also be executed as a CLI:

    python -m anagram_finder WORD CANDIDATE...

It will print each matching anagram on its own line.
"""

from __future__ import annotations

import argparse
from typing import Iterable, List


def find_anagrams(word: str, candidates: Iterable[str]) -> List[str]:
    """Return candidates that are anagrams of word, excluding identical word."""
    sorted_word = sorted(word)
    result: List[str] = []
    for candidate in candidates:
        if candidate == word:
            continue
        if sorted(candidate) == sorted_word:
            result.append(candidate)
    return result


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="anagram_finder",
        description="Print matching anagrams from the provided candidates.",
    )
    parser.add_argument("word", help="Word to find anagrams for")
    parser.add_argument(
        "candidates",
        nargs="+",
        help="One or more candidate words to test",
    )
    args = parser.parse_args(argv)

    for match in find_anagrams(args.word, args.candidates):
        print(match)


if __name__ == "__main__":
    main()
