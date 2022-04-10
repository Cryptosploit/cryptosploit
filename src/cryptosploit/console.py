from cmd import Cmd
from importlib import import_module
from os import path, chdir
from re import compile, error
from subprocess import Popen, PIPE
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
    variables = None

    def preloop(self):
        local_version = version("cryptosploit_modules")
        # package_version = loads(urlopen("https://pypi.org/pypi/cryptosploit_modules/json").read())["info"]["version"]
        package_version = local_version
        if local_version != package_version:
            print("There is a new version of cryptosploit_modules, please run:")
            print("pip install cryptosploit_modules --upgrade")

    def onecmd(self, line: str) -> bool:
        try:
            return super().onecmd(line)
        except CryptoException as err:
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
        csmodule = get_loader("cryptosploit_modules")
        modules = (name for _, name, _ in
                   walk_packages(
                       [path.dirname(csmodule.path)], csmodule.name + "."
                   ))
        try:
            r = compile(pattern)
            found = list(map(lambda a: a.split(".", 1)[1], filter(r.match, modules)))
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
        name, value = arg.split(maxsplit=1)
        if self.variables:
            if name in self.variables:
                self.variables.set_var(name, value)
                print(f"Setting {name} -> {value}")
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
