#!./venv/bin/python
from .commands import allowed_commands, EMPTY_COMMAND
from .exceptions import ArgError
from . import BS, message_handler

# TODO: add a handler of module funcs


def get_command():
    command = input("crsconsole> ")
    return command


def parse_command(command: str) -> tuple:
    command, *args = command.split()
    err_msg = ""
    def argerror_msg(amount):
        nonlocal err_msg
        err_msg = f"[!] Error: {amount} arguments required"
    
    if command not in allowed_commands.keys():
        BS.run_command(" ".join(([command]+args)))
        return EMPTY_COMMAND, args
    else:
        command = allowed_commands[command]
        if len(args) != command.args_amount:
            argerror_msg(command.args_amount)
    if err_msg:
        raise ArgError(err_msg)
    else:
        return command, args
