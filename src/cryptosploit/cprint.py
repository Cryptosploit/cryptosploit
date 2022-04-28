class SGR:
    """Styling class with constants."""
    TEMPLATE = "\x1b[{}m"
    CLEAR = TEMPLATE.format("0")

    @staticmethod
    def format(s):
        return SGR.TEMPLATE.format(s)

    class STYLES:
        NORMAL = "0"
        BOLD = "1"
        LIGHT = "2"
        ITALIC = "3"
        UNDERLINE = "4"
        BLINK = "5"

    class COLOR:
        class FOREGROUND:
            BLACK = "30"
            RED = "31"
            GREEN = "32"
            YELLOW = "33"
            BLUE = "34"
            PURPLE = "35"
            CYAN = "36"
            WHITE = "37"

        class BACKGROUND:
            BLACK = "40"
            RED = "41"
            GREEN = "42"
            YELLOW = "43"
            BLUE = "44"
            PURPLE = "45"
            CYAN = "46"
            WHITE = "47"


def colorize_strings(*strings, styles=[], fg="", bg="", sep=" "):
    """
    With colorize_strings you can change
    strings style, color (fg), color of background (bg).
    Use SGR class for styling.
    """
    template = ""
    if styles:
        template += SGR.format(";".join(styles))
    if fg:
        template += SGR.format(fg)
    if bg:
        template += SGR.format(bg)
    template += "{}" + SGR.CLEAR
    return template.format(sep.join(map(template.format, strings)))


class Printer:
    """
    Class for printing of any information.
    Use it to colorize the output of your module.
    """
    @staticmethod
    def info(*strings, sep=" "):
        """Print cyan string with '[>]' prefix."""
        prefix = colorize_strings("[>]", sep.join(strings), fg=SGR.COLOR.FOREGROUND.CYAN)
        print(prefix)

    @staticmethod
    def error(*strings, sep=" "):
        """Print red string with '[!]' prefix."""
        s = colorize_strings(
            colorize_strings("[!]", styles=[SGR.STYLES.BLINK]),
            sep.join(strings),
            fg=SGR.COLOR.FOREGROUND.RED,
        )
        print(s)

    @staticmethod
    def exec(*strings, sep=" "):
        """Print yellow string with '[*]' prefix."""
        prefix = colorize_strings("[*]", sep.join(strings), fg=SGR.COLOR.FOREGROUND.YELLOW)
        print(prefix)

    @staticmethod
    def positive(*strings, sep=" "):
        """Print green string with '[+]' prefix."""
        prefix = colorize_strings("[+]", sep.join(strings), fg=SGR.COLOR.FOREGROUND.GREEN)
        print(prefix)

    @staticmethod
    def negative(*strings, sep=" "):
        """Print red string with '[-]' prefix."""
        prefix = colorize_strings("[-]", sep.join(strings), fg=SGR.COLOR.FOREGROUND.RED)
        print(prefix)
