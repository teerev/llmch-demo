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
