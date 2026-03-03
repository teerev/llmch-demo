from __future__ import annotations

from hangman.game import guess_letter, is_lost, is_won, masked_word, new_game


def run_game(input_stream, output_stream, secret_word: str, max_attempts: int) -> str:
    """Run an interactive hangman game.

    Reads guesses from input_stream and writes prompts/results to output_stream.
    Returns "won" or "lost".
    """
    state = new_game(secret_word, max_attempts)

    while not is_won(state) and not is_lost(state):
        output_stream.write(f"Word: {masked_word(state)}\n")

        line = input_stream.readline()
        if line == "":
            # EOF: stop and treat as lost
            break

        stripped = line.strip()
        if stripped == "":
            continue

        guess_letter(state, stripped[0])

    if is_won(state):
        output_stream.write(f"You win! The word was {state.secret_word}.\n")
        return "won"

    output_stream.write(f"You lose! The word was {state.secret_word}.\n")
    return "lost"
