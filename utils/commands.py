from subprocess import Popen, PIPE

from . import message_handler, change_cwd


class Command:
    def __init__(self, args_amount, executor):
        self.args_amount = args_amount
        self.executor = executor

    def exec(self, *args):
        self.executor(*args)


@message_handler()
def use_executor(path):
    # check module exists
    yield "No such module"


@message_handler()
def search_executor(name):
    # find modules
    yield "No such module"


@message_handler()
def exit_executor():
    yield "Bye bye! UwU"
    exit(0)


@message_handler()
def set_executor(name, value):
    # find modules
    yield f"{name} -> {value}"


@message_handler()
def options_executor():
    yield "show options"


@message_handler()
def run_executor():
    # find modules
    yield "Successful"


@message_handler()
def change_directory(path: str):
    yield f"[*] Executing cd {path}"
    change_cwd(path)


@message_handler(end="")
def run_command(command: str):
    proc = Popen(command, stderr=PIPE, shell=True, stdin=PIPE, stdout=PIPE, universal_newlines=True)
    yield f"[*] Executing '{command}'\n"
    for line in iter(proc.stdout.readline, ""):
        yield line
    return_code = proc.wait()
    if return_code == 127:
        yield "[!] Unknown command\n"
    else:
        for line in iter(proc.stderr.readline, ""):
            yield line
        proc.stderr.close()


allowed_commands = {
    "use": Command(1, use_executor),
    "search": Command(1, search_executor),
    "exit": Command(0, exit_executor),
    "set": Command(2, set_executor),
    "options": Command(0, options_executor),
    "run": Command(0, run_executor),
    "cd": Command(1, change_directory)
}
BashExecutor = Command(-1, run_command)
