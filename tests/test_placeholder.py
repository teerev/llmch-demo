def test_placeholder_import_and_main_callable():
    import hangman.cli

    assert callable(hangman.cli.main)
