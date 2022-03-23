def message_handler(end="\n"):
    def wrap(func):
        def inner(*args, **kwargs):
            for line in func(*args, **kwargs):
                print(line, end=end)

        return inner

    return wrap


class CryptoSploit:
    """
    Framework class
    """


CS = CryptoSploit()
