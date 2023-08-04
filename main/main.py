from cli import parse_cli_arguments
from mp import play_with_threading


def main():
    args = parse_cli_arguments()
    play_with_threading(args)


if __name__ == '__main__':
    main()
