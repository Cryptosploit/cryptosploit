#!./venv/bin/python

# TODO: add a handler of module funcs

class ArgError(Exception):
    """
    Exception raised for errors in the input command.
    """

    def __init__(self, message: str):
        super().__init__(message)


allowed_commands = {
    "use": 1,
    "search": 1,
    "exit": 0,
    "set": 2,
    "options": 0,
    "run": 0
}


def parse_command(command: str) -> tuple:
    command, *args = command.split()
    err_msg = ""
    if command not in allowed_commands.keys():
        err_msg = "Unknown command"
    elif len(args) > allowed_commands[command.lower()]:
        err_msg = "Too much args"
    elif len(args) < allowed_commands[command.lower()]:
        err_msg = "Not enough args"
    if not err_msg:
        return command, args
    else:
        raise ArgError(err_msg)
