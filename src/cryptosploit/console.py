from cmd import Cmd

from . import allowed_commands, BashExecutor
from .exceptions import CryptoException


class CRSConsole(Cmd):
    """
    Class of main console
    """
    prompt = "crsconsole> "
    intro = "Wellcome to CryptoSploit <3"

    def default(self, command: str) -> bool:
        try:
            command, args = self.parse_command(command)
            return command.exec(*args)
        except CryptoException as err:
            print(str(err))
            return False

    @staticmethod
    def parse_command(command: str) -> tuple:
        command, *args = command.split(maxsplit=1) + [""]
        args = args[0]
        if command not in allowed_commands.keys():
            return BashExecutor, [f"{command} {args}"]
        else:
            command = allowed_commands[command]
            args = args.split(maxsplit=command.args_amount - 1)
            return command, args
