from cmd import Cmd

from . import message_handler
from .exceptions import CryptoException
from .handlers import parse_command


class CRSConsole(Cmd):
    """
    Class of main console
    """
    prompt = "crsconsole> "

    
    def default(self, command: str) -> bool:
        try:
            # command = Command(command)
            # command.exec()
            command, args = parse_command(command)
            command.exec(*args)
        except CryptoException as err:
            print(str(err))
        return True