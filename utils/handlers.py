#!./venv/bin/python
from .commands import allowed_commands
from .exceptions import ArgError


# TODO: add a handler of module funcs


def get_command():
    command = input("crsconsole> ")
    return command


def parse_command(command: str) -> tuple:
    command, *args = command.split()
    err_msg = ""
    if command not in allowed_commands.keys():
        # TODO: run subprocess with command
        err_msg = "Unknown command"
    else:
        command = allowed_commands[command]
        if len(args) > command.args_amount:
            err_msg = "Too many args"
        elif len(args) < command.args_amount:
            err_msg = "Not enough args"
    if not err_msg:
        return command, args
    else:
        raise ArgError(err_msg)
