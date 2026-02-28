import sys
import random

from .game import HangmanGame
from .words import WORDS


def main(input_stream=None, output_stream=None, word_list=None, rng=None, max_misses=6):
    if input_stream is None:
        input_stream = sys.stdin
    if output_stream is None:
        output_stream = sys.stdout
    if word_list is None:
        word_list = WORDS
    if rng is None:
        rng = random.Random()

    secret = rng.choice(word_list)
    game = HangmanGame(secret, max_misses=max_misses)

    print('Welcome to Hangman!', file=output_stream)

    while not game.is_won() and not game.is_lost():
        print(f'Word: {game.masked_word()}', file=output_stream)
        print(f'Misses: {len(game.missed_guesses)}/{game.max_misses}', file=output_stream)
        output_stream.write('Guess a letter: ')
        output_stream.flush()

        line = input_stream.readline()
        if line == '':
            break

        guess = line.strip()
        if len(guess) != 1 or not guess.isalpha():
            print('Invalid guess.', file=output_stream)
            continue

        guess = guess.lower()
        if guess in game.correct_guesses or guess in game.missed_guesses:
            print('Already guessed.', file=output_stream)
            continue

        if game.guess(guess):
            print('Correct!', file=output_stream)
        else:
            print('Incorrect.', file=output_stream)

    if game.is_won():
        print(f'You won! The word was {game.secret_word}.', file=output_stream)
    elif game.is_lost():
        print(f'You lost! The word was {game.secret_word}.', file=output_stream)
    else:
        print('Game ended.', file=output_stream)
