#!./venv/bin/python
from utils.exceptions import CryptoException
from utils.handlers import parse_command, get_command


def main():
    while True:
        try:
            command = get_command()
            command, args = parse_command(command)
            command.exec(*args)
        except KeyboardInterrupt:
            print("\nType 'exit' to quit")
        except CryptoException as err:
            print(str(err))


if __name__ == "__main__":
    main()
