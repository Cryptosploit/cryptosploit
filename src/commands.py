from inspect import getfullargspec
from os import path, chdir
from subprocess import Popen, PIPE

from .exceptions import PathError

allowed_commands = dict()


def allow(name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        allowed_commands[name] = Command(func)
        return wrapper

    return decorator


class Command:
    """
    Class of custom crsconsole commands
    """

    def __init__(self, executor):
        self.executor = executor
        self.args_amount = len(getfullargspec(executor).args)

    def exec(self, *args):
        return self.executor(*args)


@allow("use")
def use_executor(module_path):
    # check module exists
    print("No such module")
    return False


@allow("search")
def search_executor(name):
    # find modules
    print("No such module")
    return False


@allow("exit")
def exit_executor():
    print("Bye bye! UwU")
    return True


@allow("set")
def set_executor(name, value):
    # find modules
    print(f"{name} -> {value}")
    return False


@allow("options")
def options_executor():
    print("show options")
    return False


@allow("run")
def run_executor():
    # find modules
    print("Successful")
    return False


@allow("cd")
def cd_executor(new_path: str):
    print(f"[*] Executing cd {new_path}")
    cwd = path.abspath(new_path)
    if path.exists(cwd):
        chdir(cwd)
    else:
        raise PathError("[!] No such directory")
    return False


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
    return False


BashExecutor = Command(run_shell_command)
