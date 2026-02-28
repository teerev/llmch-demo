import io
import random

from hangman import cli


def test_cli_win_simple():
    out = io.StringIO()
    cli.main(
        input_stream=io.StringIO('h\ni\n'),
        output_stream=out,
        word_list=['hi'],
        rng=random.Random(0),
        max_misses=6,
    )
    s = out.getvalue()
    assert 'Welcome to Hangman!' in s
    assert 'Word: __' in s
    assert 'You won! The word was hi.' in s
