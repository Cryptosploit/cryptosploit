from cmd import Cmd
from importlib import import_module
from importlib.util import find_spec
from inspect import getfile
import os
from os import chdir, listdir
from re import compile, error
from subprocess import Popen, PIPE
from sys import path
from pkgutil import walk_packages, get_loader

from .banners import print_banner
from .cprint import colorize_strings, SGR, Printer
from .exceptions import (
    ArgError,
    CryptoException,
    PathError,
    ModuleError,
    UnknownCommandError,
)


class CRSConsole(Cmd):
    """
    Class of main console
    """

    prompt = "crsconsole> "
    intro = (
        "Wellcome to CryptoSploit "
        + colorize_strings("<3", fg=SGR.COLOR.FOREGROUND.RED)
        + "\nType "
        + colorize_strings("help", fg=SGR.COLOR.FOREGROUND.GREEN)
        + " or "
        + colorize_strings("?", fg=SGR.COLOR.FOREGROUND.GREEN)
        + " to list commands.\n"
    )

    module = None
    modules_list = None
    variables = None
    shell_proc: Popen | None = None

    def load_modules(self):
        csmodule = get_loader("cryptosploit_modules")
        self.modules_list = list(
            map(
                lambda x: x.split(".", 1)[1],
                (
                    name
                    for _, name, ispkg in walk_packages(
                        [os.path.dirname(csmodule.path)], csmodule.name + "."
                    )
                    if ispkg
                ),
            )
        )

    def preloop(self):
        self.load_modules()
        print_banner()
        path.insert(0, find_spec("cryptosploit_modules").submodule_search_locations[0])

    def precmd(self, line: str) -> str:
        if line == "EOF":
            print()
            return ""
        return line

    def onecmd(self, line: str) -> bool:
        try:
            return super().onecmd(line)
        except CryptoException as err:
            Printer.error(str(err))
            return False
        except KeyboardInterrupt:
            print()
            if self.module:
                self.module.kill_proc()
            if self.shell_proc:
                self.shell_proc.terminate()
                self.shell_proc.kill()
                self.shell_proc = None

    def default(self, line: str) -> bool:
        self.do_shell(line)
        return False

    def emptyline(self) -> bool:
        return False

    def do_shell(self, arg):
        """
        Any shell command.
        Example: ls -la
        """
        self.shell_proc = Popen(
            arg,
            shell=True,
            stdin=self.stdin,
            stdout=self.stdout,
            stderr=PIPE,
            universal_newlines=True,
        )
        Printer.exec(f"Executing '{arg}'")
        return_code = self.shell_proc.wait()
        if return_code == 127:
            raise UnknownCommandError("Unknown command")
        for line in iter(self.shell_proc.stderr.readline, ""):
            print(line, end="")
        return False

    def do_use(self, module_path: str):
        """
        Load module
        Example: use symmetric.rot
        """
        try:
            self.module = import_module("cryptosploit_modules." + module_path).module
            venv_path = os.path.join(
                os.path.dirname(getfile(self.module.__class__)), "venv"
            )
            for root, dirs, _ in os.walk(venv_path):
                if "site-packages" in dirs:
                    path[0] = os.path.join(root, "site-packages")
                    break
            else:
                path[0] = ""
            self.variables = self.module.env
            self.prompt = f"crsconsole {colorize_strings(f'({module_path})', fg=SGR.COLOR.FOREGROUND.PURPLE)}> "
            Printer.info("Module loaded successfully")
        except ModuleNotFoundError:
            raise ModuleError("No such module")
        except AttributeError:
            raise ModuleError("Not a module")
        return False

    def do_search(self, name):
        """
        Search modules by keyword.
        Example: search rot
        """
        pattern = f".*{name}.*"
        try:
            r = compile(pattern)
            found = list(filter(r.match, self.modules_list))
            Printer.info("\n".join(found) if found else f"No results for {name}")
            return False
        except error:
            raise ArgError("Invalid regex")

    def do_exit(self, arg=""):
        """
        Just an exit command.
        Just type exit.
        """
        print("Bye bye! UwU")
        return True

    def do_run(self, arg):
        """
        Run loaded module.
        Just type run.
        """
        self.module.run()
        return False

    def do_set(self, arg):
        """
        Set the value of a variable.
        Example: set ciphertext OwO
        """
        arg = arg.split(maxsplit=1)
        if len(arg) == 2:
            name, value = arg
            if self.variables:
                if name in self.variables:
                    self.variables.set_var(name, value)
                    Printer.info(f"Setting {name} -> {value}")
                    return False
                raise ArgError("No such variable")
            raise ModuleError("Module is not loaded")
        raise ArgError("Value is not set")

    def do_unset(self, name):
        """
        Unset the value of a variable.
        Example: unset ciphertext
        """
        if self.variables:
            if name in self.variables:
                self.variables.set_var(name, "")
                Printer.info(f"Setting {name} -> None")
                return False
            raise ArgError("No such variable")
        raise ModuleError("Module is not loaded")

    def do_get(self, arg):
        """
        Print variables allowed to set.
        Just type get.
        """
        if self.variables:
            print(self.variables)
            return False
        raise ModuleError("Module is not loaded")

    def do_cd(self, new_path: str):
        """
        Wrapper over change directory command.
        Use like cd.
        """
        Printer.exec(f"Executing cd {new_path}")
        cwd = os.path.abspath(new_path)
        if os.path.exists(cwd):
            chdir(cwd)
        else:
            raise PathError("No such directory")
        return False

    def completedefault(self, text, line, begidx, endidx):
        return self.explore_paths(line, False)

    def complete_cd(self, text, line, begidx, endidx):
        return self.explore_paths(line, True)

    @staticmethod
    def explore_paths(line, only_dirs):
        text = (line.split(" "))[-1]
        if text in ("..", "."):
            return (
                [os.path.join(".", ""), os.path.join("..", "")]
                if text == "."
                else [os.path.join("..", "")]
            )
        if only_dirs:
            paths = filter(
                lambda x: os.path.isdir(os.path.join(os.path.dirname(text), x)),
                listdir(os.path.dirname(text) or "."),
            )
        else:
            paths = listdir(os.path.dirname(text) or ".")
        founded = list(
            map(
                lambda a: os.path.join(a, "") if os.path.isdir(a) else a,
                filter(lambda x: x.startswith(os.path.split(text)[-1]), paths),
            )
        )
        return founded

    def complete_use(self, text, line, begidx, endidx):
        return self.complete_search(text, line, begidx, endidx)

    def complete_search(self, text, line, begidx, endidx):
        founded = list(
            filter(
                lambda x: x.startswith(text) and len(x.split(".")) > 1,
                self.modules_list,
            )
        )
        return founded

    def complete_set(self, text, line, begidx, endidx):
        if " " not in line[:begidx].strip():
            founded = []
            if self.variables:
                for varname in iter(self.variables):
                    if varname.startswith(text):
                        founded.append(varname)
                return founded
        else:
            return self.explore_paths(line, False)

    def complete_unset(self, text, line, begidx, endidx):
        return self.complete_set(text, line, begidx, endidx)
