from .cli import main as _cli_main


def main(**kwargs):
    return _cli_main(**kwargs)


if __name__ == '__main__':
    main()
