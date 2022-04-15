from cmd import Cmd
from importlib import import_module
from os import path, chdir, listdir, getcwd
from re import compile, error
from subprocess import Popen, PIPE
from traceback import format_exc
from pkgutil import walk_packages, get_loader
from importlib.metadata import version
# from json import loads
# from urllib.request import urlopen

from .exceptions import ArgError, CryptoException, PathError, ModuleError, UnknownCommandError


class CRSConsole(Cmd):
    """
    Class of main console
    """
    prompt = "crsconsole> "
    intro = "Wellcome to CryptoSploit <3\nType help or ? to list commands.\n"
    module = None
    modules_list = None
    variables = None

    def load_modules(self):
        csmodule = get_loader("cryptosploit_modules")
        self.modules_list = list(map(lambda x: x.split(".", 1)[1],
                                     (name for _, name, ispkg in walk_packages(
                                         [path.dirname(csmodule.path)], csmodule.name + ".") if ispkg)))

    def check_update(self):
        local_version = version("cryptosploit_modules")
        # package_version = loads(urlopen("https://pypi.org/pypi/cryptosploit_modules/json").read())["info"]["version"]
        package_version = local_version
        if local_version != package_version:
            print("A new version of cryptosploit_modules is available! Update with:")
            print("pip install cryptosploit_modules --upgrade")

    def preloop(self):
        self.check_update()
        self.load_modules()

    def precmd(self, line: str) -> str:
        if line == "EOF":
            print()
            return ""
        return line

    def onecmd(self, line: str) -> bool:
        try:
            return super().onecmd(line)
        except CryptoException as err:
            print(format_exc()) # to remove
            print(str(err))
            return False

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
        proc = Popen(arg, stderr=PIPE, shell=True, stdin=PIPE, stdout=PIPE, universal_newlines=True, text=True)
        print(f"[*] Executing '{arg}'")
        for line in iter(proc.stdout.readline, ""):
            print(line, end="")
        return_code = proc.wait()
        if return_code == 127:
            raise UnknownCommandError("[!] Unknown command")
        else:
            for line in iter(proc.stderr.readline, ""):
                print(line, "\n")
            proc.stderr.close()
        return False

    def do_use(self, module_path: str):
        """
        Load module
        Example: use symmetric.rot
        """
        try:
            self.module = import_module("cryptosploit_modules." + module_path).module
            self.variables = self.module.env
            self.prompt = f"crsconsole ({module_path})> "
            print("Module loaded successfully")
        except ModuleNotFoundError:
            raise ModuleError("[!] No such module")
        except AttributeError:
            raise ModuleError("[!] Not a module")
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
            print("\n".join(found) if found else f"No results for {name}")
            return False
        except error:
            raise ArgError("Invalid regex")

    def do_exit(self, arg):
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
                    print(f"Setting {name} -> {value}")
                    return False
                else:
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
                print(f"Setting {name} -> None")
                return False
            else:
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
        print(f"[*] Executing cd {new_path}")
        cwd = path.abspath(new_path)
        if path.exists(cwd):
            chdir(cwd)
        else:
            raise PathError("[!] No such directory")
        return False

    def completedefault(self, text, line, begidx, endidx):
        return self.explore_paths(line, False)

    def complete_cd(self, text, line, begidx, endidx):
        return self.explore_paths(line, True)

    @staticmethod
    def explore_paths(line, only_dirs):
        text = (line.split(" "))[-1]
        if text in ("..", "."):
            return [path.join(".", ""), path.join("..", "")] if text == "." else [path.join("..", "")]
        if only_dirs:
            paths = filter(lambda x: path.isdir(path.join(path.dirname(text), x)), listdir(path.dirname(text) or "."))
        else:
            paths = listdir(path.dirname(text) or ".")
        founded = list(map(lambda a: path.join(a, "") if path.isdir(a) else a,
                           filter(lambda x: x.startswith(path.split(text)[-1]), paths)))
        return founded

    def complete_use(self, text, line, begidx, endidx):
        return self.complete_search(text, line, begidx, endidx)

    def complete_search(self, text, line, begidx, endidx):
        founded = list(filter(lambda x: x.startswith(text) and len(x.split(".")) > 1, self.modules_list))
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
