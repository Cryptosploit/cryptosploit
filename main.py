#!./venv/bin/python
from utils import message_handler
from utils.exceptions import CryptoException
from utils.handlers import parse_command, get_command


@message_handler()
def main():
    while True:
        try:
            command = get_command()
            command, args = parse_command(command)
            command.exec(*args)
        except KeyboardInterrupt:
            yield "\nType 'exit' to quit"
        except CryptoException as err:
            yield str(err)


if __name__ == "__main__":
    main()
