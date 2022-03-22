#!./venv/bin/python
from utils import parse_command, ArgError


# TODO: add crptsploit command execution
# TODO: add bash command parsing and execution

def get_command():
    command = input("crptsploit> ")
    return command


def main():
    while True:
        try:
            command = get_command()
            if command == "exit":
                return
            parse_command(command)
            print(command)
        except KeyboardInterrupt:
            print("\nType 'exit' to quit")
        except ArgError as err:
            print(str(err))


main()
