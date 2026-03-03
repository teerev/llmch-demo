from __future__ import annotations

from io import StringIO

from hangman.__main__ import main


def test_main_win_outcome_and_message() -> None:
    # Provide exact guesses to win.
    input_stream = StringIO("p\ny\nt\nh\no\nn\n")
    output_stream = StringIO()

    outcome = main(
        argv=["--word", "python", "--max-attempts", "6"],
        input_stream=input_stream,
        output_stream=output_stream,
    )

    assert outcome == "won"
    out = output_stream.getvalue()
    assert "You win! The word was python." in out
