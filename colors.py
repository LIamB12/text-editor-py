import curses

def init_rose_pine():
    
    BASE = {"num": 8, "hex": "#191724"}
    SURFACE = {"num": 2, "hex": "#1f1d2e"}
    OVERLAY = {"num": 10, "hex": "#26233a"}
    MUTED = {"num": 9, "hex": "#6e6a86"}
    SUBTLE = {"num": 3, "hex": "#908caa"}
    TEXT = {"num": 6, "hex": "#e0def4"}
    LOVE = {"num": 7, "hex": "#eb6f92"}
    GOLD = {"num": 1, "hex": "#f6c177"}
    ROSE = {"num": 5, "hex": "#ebbcba"}
    PINE = {"num": 4, "hex": "#31748f"}
    FOAM = {"num": 11, "hex": "#9ccfd8"}
    IRIS = {"num": 6, "hex": "#c4a7e7"}
    HIGHLIGHT_LOW = {"num": 13, "hex": "#21202e"}
    HIGHLIGHT_MED = {"num": 14, "hex": "#403d52"}
    HIGHLIGHT_HIGH = {"num": 15, "hex": "#524f67"}

    curses.start_color()
    curses.use_default_colors()

    add_curses_color(BASE)
    add_curses_color(SURFACE)
    add_curses_color(OVERLAY)
    add_curses_color(MUTED)
    add_curses_color(SUBTLE)
    add_curses_color(TEXT)
    add_curses_color(LOVE)
    add_curses_color(GOLD)
    add_curses_color(ROSE)
    add_curses_color(PINE)
    add_curses_color(FOAM)
    add_curses_color(IRIS)
    add_curses_color(HIGHLIGHT_LOW)
    add_curses_color(HIGHLIGHT_MED)
    add_curses_color(HIGHLIGHT_HIGH)

def init_white():
    
    BASE = {"num": 8, "hex": "#e0def4"}
    SURFACE = {"num": 2, "hex": "#e0def4"}
    OVERLAY = {"num": 10, "hex": "#e0def4"}
    MUTED = {"num": 9, "hex": "#6e6a86"}
    SUBTLE = {"num": 3, "hex": "#e0def4"}
    TEXT = {"num": 6, "hex": "#e0def4"}
    LOVE = {"num": 7, "hex": "#e0def4"}
    GOLD = {"num": 1, "hex": "#e0def4"}
    ROSE = {"num": 5, "hex": "#e0def4"}
    PINE = {"num": 4, "hex": "#e0def4"}
    FOAM = {"num": 11, "hex": "#e0def4"}
    IRIS = {"num": 6, "hex": "#e0def4"}
    HIGHLIGHT_LOW = {"num": 13, "hex": "#e0def4"}
    HIGHLIGHT_MED = {"num": 14, "hex": "#e0def4"}
    HIGHLIGHT_HIGH = {"num": 15, "hex": "#e0def4"}

    curses.start_color()
    curses.use_default_colors()

    add_curses_color(BASE)
    add_curses_color(SURFACE)
    add_curses_color(OVERLAY)
    add_curses_color(MUTED)
    add_curses_color(SUBTLE)
    add_curses_color(TEXT)
    add_curses_color(LOVE)
    add_curses_color(GOLD)
    add_curses_color(ROSE)
    add_curses_color(PINE)
    add_curses_color(FOAM)
    add_curses_color(IRIS)
    add_curses_color(HIGHLIGHT_LOW)
    add_curses_color(HIGHLIGHT_MED)
    add_curses_color(HIGHLIGHT_HIGH)






def add_curses_color(color):

    R = int("0x" + color["hex"][1:3], 16)
    G = int("0x" + color['hex'][3:5], 16)
    B = int("0x" + color["hex"][5:], 16)

    curses.init_color(
        color['num'],
        R * 1000 // 0xff,
        G * 1000 // 0xff,
        B * 1000 // 0xff
    )
    
    curses.init_pair(color['num'], color["num"], -1)


class lowercase:
    pass
