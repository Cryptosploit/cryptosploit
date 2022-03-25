from cmd import Cmd

from . import message_handler
from .exceptions import CryptoException
from .handlers import parse_command


class CRSConsole(Cmd):
    prompt = "crsconsole> "

    def __init__(self, intro, completekey='tab', stdin=None, stdout=None):
        print(intro)
        super(CRSConsole, self).__init__(completekey, stdin, stdout)

    def emptyline(self) -> bool:
        return False

    def precmd(self, line: str) -> str:
        if line == "EOF":
            print()
            try:
                while (answer := input("Do you really want to exit ([y]/n)? ").lower() or "y") not in ("y", "n"):
                    pass
            except (EOFError, KeyboardInterrupt):
                print()
                answer = "y"
            match answer:
                case "y":
                    line = "exit"
                case "n":
                    line = ""
        return line

    @message_handler()
    def default(self, command: str) -> bool:
        try:
            command, args = parse_command(command)
            command.exec(*args)
        except CryptoException as err:
            yield str(err)
        return True

    @message_handler()
    def cmdloop(self, intro=None) -> None:
        while True:
            try:
                super(CRSConsole, self).cmdloop()
            except KeyboardInterrupt:
                yield "\nType 'exit' to quit"
