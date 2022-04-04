from subprocess import Popen, PIPE
from inspect import getfullargspec

from . import message_handler, change_cwd


class Command:
    """
    Class of custom crsconsole commands
    """

    def __init__(self, executor):
        self.executor = executor
        self.args_amount = len(getfullargspec(executor).args)

    def exec(self, *args):
        self.executor(*args)


def use_executor(path):
    # check module exists
    print("No such module")


def search_executor(name):
    # find modules
    print("No such module")


def exit_executor():
    print("Bye bye! UwU")
    exit(0)


def set_executor(name, value):
    # find modules
    print(f"{name} -> {value}")


def options_executor():
    print("show options")


def run_executor():
    # find modules
    print("Successful")


def cd_executor(path: str):
    print(f"[*] Executing cd {path}")
    change_cwd(path)


def run_shell_command(command: str):
    proc = Popen(command, stderr=PIPE, shell=True, stdin=PIPE, stdout=PIPE, universal_newlines=True)
    print(f"[*] Executing '{command}'\n")
    for line in iter(proc.stdout.readline, ""):
        print(line, end="")
    return_code = proc.wait()
    if return_code == 127:
        print("[!] Unknown command")
    else:
        for line in iter(proc.stderr.readline, ""):
            print(line, "\n")
        proc.stderr.close()


allowed_commands = {
    "use": use_executor,
    "search": search_executor,
    "exit": exit_executor,
    "set": set_executor,
    "options": options_executor,
    "run": run_executor,
    "cd": cd_executor
}

BashExecutor = Command(run_shell_command)
