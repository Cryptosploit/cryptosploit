from subprocess import Popen, PIPE
from os import getcwd, path
from .exceptions import PathError

def message_handler(end="\n"):
    def wrap(func):
        def inner(*args, **kwargs):
            for line in func(*args, **kwargs):
                print(line, end=end)

        return inner

    return wrap


class BashSession:
    def __init__(self):
        self.cwd = getcwd()
    
    def change_cwd(self, cwd: str):
        if path.exists(cwd):
            self.cwd = cwd
        else:
            raise PathError("[!] No such directory")

    @message_handler(end="")
    def run_command(self, command: str):
        proc = Popen(command, stderr=PIPE, shell=True, stdin=PIPE, stdout=PIPE, cwd=self.cwd, universal_newlines=True)
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


class CryptoSploit:
    """
    Framework class
    """


CS = CryptoSploit()
BS = BashSession()