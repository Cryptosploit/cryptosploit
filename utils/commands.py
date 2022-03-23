from . import message_handler


# TODO: make executors


class Command:
    def __init__(self, args_amount, executor):
        self.args_amount = args_amount
        self.executor = executor

    def exec(self, *args):
        self.executor(*args)


@message_handler
def use_executor(path):
    # check module exists
    yield "No such module"


@message_handler
def search_executor(name):
    # find modules
    yield "No such module"


@message_handler
def exit_executor(name):
    yield "Bye bye! UwU"
    exit(0)


@message_handler
def set_executor(name, value):
    # find modules
    yield f"{name} -> {value}"


@message_handler
def run_executor(name):
    # find modules
    yield "Successful"


use_command = Command(1, use_executor)

allowed_commands = {
    "use": use_command,
    "search": 1,
    "exit": 0,
    "set": 2,
    "options": 0,
    "run": 0
}
