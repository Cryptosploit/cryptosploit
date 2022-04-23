class SGR:
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
    template = ""
    if styles:
        template += SGR.format(";".join(styles))
    if fg:
        template += SGR.format(fg)
    if bg:
        template += SGR.format(bg)
    template += "{}" + SGR.CLEAR
    return template.format(sep).join(map(template.format, strings))


class Printer:
    @staticmethod
    def info(*s, sep=" "):
        prefix = colorize_strings("[>]", fg=SGR.COLOR.FOREGROUND.CYAN)
        print(prefix, sep.join(s))

    @staticmethod
    def error(*s, sep=" "):
        s = colorize_strings(
            colorize_strings("[!]", styles=[SGR.STYLES.BLINK]),
            sep.join(s),
            fg=SGR.COLOR.FOREGROUND.RED,
        )
        print(s)

    @staticmethod
    def exec(*s, sep=" "):
        prefix = colorize_strings("[*]", fg=SGR.COLOR.FOREGROUND.GREEN)
        print(prefix, sep.join(s))
