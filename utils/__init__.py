def message_handler(func):
    def inner(*args, **kwargs):
        for line in func(*args, **kwargs):
            print(line)

    return inner


class CryptoSploit:
    """
    Framework class
    """


CS = CryptoSploit()
