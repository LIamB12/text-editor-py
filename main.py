#!/bin/python3

import curses, sys
from typing import List

def main(stdscr):

    s = curses.initscr()
    s.nodelay(True)
    curses.noecho()
    curses.raw()
    s.keypad(True)

    buf = []
    src_file = "noname.txt"

    R, C = s.getmaxyx() # add dynamic resizing

    x, y, r, c = 0,0,0,0

    if len(sys.argv) == 2:
        src_file = sys.argv[1]

    try:
        with open(src_file) as file:

            cont = file.read().split('\n')
            cont = cont[:-1] if len(cont) > 1 else cont

            for row in cont:
                buf.append([ord(c) for c in row])

    except:
        buf.append([])

    while True:
        ch = -1
        s.move(0,0)

        # Scrolling
        if r < y:
            y = r

        if r >= y + R:
            y = r - R + 1

        if c < x:
            x = c

        if c >= x + C:
            x = c - C + 1

        #Print

        for row in range(R):
            buf_row = row + y
            for col in range(C):
                buf_col = col + x
                try:
                    s.addch(row, col, buf[buf_row][buf_col])
                except:
                    pass
            s.clrtoeol()
            try:
                s.addch('\n')
            except:
                pass

        curses.curs_set(False)
        s.move(r-y, c-x)
        curses.curs_set(True)
        s.refresh()

        while ch == -1:
            ch = s.getch()

        if ch != (ch & 0x1f) and ch < 128:
            buf[r].insert(c, ch)
            c += 1
        elif chr(ch) in '\n\r': # handle enter
            line = buf[r][c:]
            buf [r] = buf[r][:c]
            r += 1
            c = 0
            buf.insert(r, [] + line)
        elif ch in [8, 263]: # Backspace
            if c > 0:
                c -= 1
                del buf[r][c]
            elif r > 0:
                line = buf[r]
                del buf[r]
                r -= 1
                prev_line_len = len(buf[r])
                buf[r] += line
                c = prev_line_len
        elif ch == curses.KEY_RIGHT:
            if c < len(buf[r]):
                c += 1
            elif r < len(buf) - 1:
                r += 1
                c = 0
        elif ch == curses.KEY_LEFT:
            if c > 0:
                c -= 1
            elif r > 0:
                r -= 1
                c = len(buf[r])
        elif ch == curses.KEY_UP and r != 0:
            r -= 1
        elif ch == curses.KEY_DOWN and r < len(buf) - 1:
            r += 1

        if ch == (ord("q") & 0x1f): #Ctrl-Q quits
            sys.exit()
        
        if ch == (ord("s") & 0x1f): #Ctrl-S quits
            cont = ''
            for line in buf:
                for ascii_char in line:
                    cont += chr(ascii_char)
                cont += '\n'

            with open(src_file, "w") as file:
                file.write(cont)
        
        row = buf[r] if r < len(buf) else None
        row_len = len(row) if row is not None else 0
        if c > row_len:
            c = row_len

curses.wrapper(main)
