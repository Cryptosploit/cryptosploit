from importlib.metadata import version
from json import loads
from urllib.request import urlopen

from .console import CRSConsole


def check_update():
    local_version = version("cryptosploit_modules")
    # package_version = loads(urlopen("https://pypi.org/pypi/cryptosploit_modules/json").read())["info"]["version"]
    package_version = local_version
    if local_version != package_version:
        print("There is a new version of cryptosploit_modules, please run:")
        print("pip install cryptosploit_modules --upgrade")


def main():
    check_update()
    console = CRSConsole()
    console.cmdloop()
