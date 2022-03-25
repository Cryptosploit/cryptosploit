#!./venv/bin/python
from .commands import allowed_commands, BashExecutor
from .exceptions import ArgError

# TODO: add a handler of module funcs


def parse_command(command: str) -> tuple:
    command, *args = command.split()
    err_msg = ""
    if command not in allowed_commands.keys():
        return BashExecutor, [" ".join(([command] + args))]
    else:
        command = allowed_commands[command]
        if len(args) != command.args_amount:
            err_msg = f"[!] Error: {command.args_amount} arguments required"
    if err_msg:
        raise ArgError(err_msg)
    else:
        return command, args
