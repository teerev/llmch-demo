class HangmanGame:
    def __init__(self, secret_word: str, max_misses: int = 6):
        if not secret_word:
            raise ValueError("secret_word must not be empty")
        if max_misses < 0:
            raise ValueError("max_misses must be >= 0")

        self.secret_word = secret_word.lower()
        self.max_misses = max_misses
        self.correct_guesses = set()
        self.missed_guesses = set()

    def masked_word(self) -> str:
        masked = []
        for ch in self.secret_word:
            if ch.isalpha():
                masked.append(ch if ch in self.correct_guesses else "_")
            else:
                masked.append(ch)
        return "".join(masked)

    def guess(self, letter: str) -> bool:
        if letter is None or not isinstance(letter, str) or len(letter) != 1 or not letter.isalpha():
            raise ValueError("letter must be a single alphabetic character")

        letter = letter.lower()

        if letter in self.correct_guesses or letter in self.missed_guesses:
            return False

        if letter in self.secret_word:
            self.correct_guesses.add(letter)
            return True

        self.missed_guesses.add(letter)
        return False

    def is_won(self) -> bool:
        needed = {ch for ch in self.secret_word if ch.isalpha()}
        return needed.issubset(self.correct_guesses)

    def is_lost(self) -> bool:
        return len(self.missed_guesses) >= self.max_misses
