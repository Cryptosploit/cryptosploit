from os import path, chdir

from .exceptions import PathError, CryptoException


def message_handler(end="\n"):
    """
    Main decorator for output
    """
    def wrap(func):
        def inner(*args, **kwargs):
            for line in func(*args, **kwargs):
                print(line, end=end)

        return inner

    return wrap


def change_cwd(cwd: str):
    cwd = path.abspath(cwd)
    if path.exists(cwd):
        chdir(cwd)
    else:
        raise PathError("[!] No such directory")


class CryptoSploit:
    """
    Framework class
    """


CS = CryptoSploit()
