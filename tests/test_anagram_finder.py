from anagram_finder import find_anagrams


def test_find_anagrams_basic():
    word = "listen"
    candidates = ["enlist", "google", "inlets", "banana", "listen"]
    assert find_anagrams(word, candidates) == ["enlist", "inlets"]


def test_find_anagrams_empty_candidates():
    assert find_anagrams("listen", []) == []
