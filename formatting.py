class command_line_formats:

    class text_color:
        BLACK       = "\033[30m"
        RED         = "\033[31m"
        GREEN       = "\033[32m"
        YELLOW      = "\033[33m"
        BLUE        = "\033[34m"
        MAGENTA     = "\033[35m"
        CYAN        = "\033[36m"
        WHITE       = "\033[37m"

        GRAY_D      = "\033[90m"
        RED_L       = "\033[91m"
        GREEN_L     = "\033[92m"
        YELLOW_L    = "\033[93m"
        BLUE_L      = "\033[94m"
        PINK        = "\033[95m"
        CYAN_L      = "\033[96m"

        RESET       = "\033[39m"

    class bg_color:
        BLACK       = "\033[40m"
        RED         = "\033[41m"
        GREEN       = "\033[42m"
        YELLOW      = "\033[43m"
        BLUE        = "\033[44m"
        MAGENTA     = "\033[45m"
        CYAN        = "\033[46m"
        WHITE       = "\033[47m"
        RESET       = "\033[49m"

    class intensity:
        BRIGHT      = "\033[1m"
        DIM         = "\033[2m"
        NORMAL      = "\033[22m"

    class style:
        BOLD        = "\033[01m"
        DISABLE     = "\033[02m"
        UNDERLINE   = "\033[04m"
        REVERSE     = "\033[07m"
        STRIKE      = "\033[09m"
        INVISIBLE   = "\033[08m"

    RESET_ALL = "\033[0m"
