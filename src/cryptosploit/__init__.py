from importlib import import_module
from inspect import getfullargspec
from os import path, chdir
from subprocess import Popen, PIPE
from re import compile
from pkgutil import walk_packages, get_loader

from .exceptions import ArgError, PathError, ModuleError

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
        if len(args) != self.args_amount:
            raise ArgError(f"[!] Error: {self.args_amount} arguments required")
        return self.executor(*args)


def shell_executor(command: str):
    proc = Popen(command, stderr=PIPE, shell=True, stdin=PIPE, stdout=PIPE, universal_newlines=True)
    print(f"[*] Executing '{command}'")
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


class CryptoSploit:
    """
    Framework class
    """
    module = None
    variables = None

    @staticmethod
    @allow("use")
    def use_executor(module_path: str):
        try:
            CryptoSploit.module = import_module("cryptosploit_modules." + module_path).module
            CryptoSploit.variables = CryptoSploit.module.env
            print("Module loaded successfully")
        except AttributeError:
            raise ModuleError("No such module")
        return False

    @staticmethod
    @allow("search")
    def search_executor(name):
        pattern = f".*{name}.*"
        csmodule = get_loader("cryptosploit_modules")
        modules = (name for _, name, _ in
                   walk_packages(
                       [path.dirname(csmodule.path)], csmodule.name + "."
                   ))
        r = compile(pattern)
        found = list(map(lambda a: a.split(".", 1)[1], filter(r.match, modules)))
        print("\n".join(found) if found else f"No results for {name}")
        return False

    @staticmethod
    @allow("exit")
    def exit_executor():
        print("Bye bye! UwU")
        return True

    @staticmethod
    @allow("run")
    def run_executor():
        CryptoSploit.module.run()
        return False

    @staticmethod
    @allow("set")
    def set_executor(name, value):
        if name in CryptoSploit.variables:
            CryptoSploit.variables.set_var(name, value)
            print(f"Setting {name} -> {value}")
        else:
            print("No such variable")
        return False

    @staticmethod
    @allow("get")
    def get_all_executor():
        print(CryptoSploit.variables)
        return False

    @staticmethod
    @allow("cd")
    def cd_executor(new_path: str):
        print(f"[*] Executing cd {new_path}")
        cwd = path.abspath(new_path)
        if path.exists(cwd):
            chdir(cwd)
        else:
            raise PathError("[!] No such directory")
        return False


BashExecutor = Command(shell_executor)
