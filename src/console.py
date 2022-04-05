from cmd import Cmd

from .commands import allowed_commands, BashExecutor
from .exceptions import CryptoException, ArgError


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
        command, *args = command.split()
        err_msg = ""
        if command not in allowed_commands.keys():
            return BashExecutor, [" ".join(([command] + args))]
        else:
            command = allowed_commands[command]
            if len(args) != command.args_amount:
                err_msg = f"[!] Error: {command.args_amount} arguments required"
        if err_msg:
            raise ArgError(err_msg)
        else:
            return command, args
