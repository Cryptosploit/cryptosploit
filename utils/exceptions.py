class CryptoException(Exception):
    """
    Base application exception
    """


class ArgError(CryptoException):
    """
    Exception raised for errors in the input command.
    """
