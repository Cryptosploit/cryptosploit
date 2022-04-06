class CryptoException(Exception):
    """
    Base application exception.
    """


class ArgError(CryptoException):
    """
    Exception raised for errors in the input command.
    """


class PathError(CryptoException):
    """
    Exception raised for errors in os paths.
    """


class ModuleError(CryptoException):
    """
    Exception raised for errors in modules.
    """