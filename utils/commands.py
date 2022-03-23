from . import message_handler


# TODO: make executors


class Command:
    def __init__(self, name, args_amount, info, executor):
        self.name = name
        self.args_amount = args_amount
        self.info = info
        self.executor = executor

    def exec(self, *args):
        self.executor(*args)

    def __str__(self):
        return self.info


@message_handler
def use_executor(path):
    # check module exists
    yield "No such module"


use_command = Command("use", 1, "", use_executor)

allowed_commands = {
    "use": use_command,
    "search": 1,
    "exit": 0,
    "set": 2,
    "options": 0,
    "run": 0
}
