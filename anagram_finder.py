"""Anagram finder core logic."""

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
