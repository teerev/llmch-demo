import io
import random
from hangman import __main__


def test_module_entrypoint_delegates():
    out = io.StringIO()
    __main__.main(
        input_stream=io.StringIO('h\ni\n'),
        output_stream=out,
        word_list=['hi'],
        rng=random.Random(0),
    )
    assert 'You won! The word was hi.' in out.getvalue()
