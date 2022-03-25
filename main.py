#!./venv/bin/python
from utils.console import CRSConsole


def main():
    console = CRSConsole(intro="Wellcome to CryptoSploit <3")
    console.cmdloop()


if __name__ == "__main__":
    main()
