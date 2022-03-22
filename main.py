#!./venv/bin/python
def get_command():
    command = input("crptsploit> ")
    if command == "exit":
        return 0
    return command


def main():
    while True:
        try:
            command = get_command()
            if command == 0:
                return
            # parse_command(command)
        except KeyboardInterrupt:
            print("\nType 'exit' to quit")


main()
