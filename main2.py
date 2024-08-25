#!/bin/python3

import curses, sys

def main():

    s = curses.initscr()
    s.nodelay(True)
    curses.noecho()
    curses.raw()
    curses.set_escdelay(1)
    s.keypad(True)

    buf = []
    src_file = "noname.txt"

    R, C = s.getmaxyx() # add dynamic resizing

    x, y, r, c = 0,0,0,0
    max_c = 0

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

    editor_state = "Insert"

    while True:
        ch = -1
        margin_l = max(len(str(len(buf))), len(str(R))) + 4

        # Scrolling
        if r < y:
            y = r

        if r >= y + R - 2:
            y = r - R + 3

        if c < x:
            x = c

        if c >= x + C:
            x = c - C + 1

        #Print

        for row in range(R - 2):
            buf_row = row + y

            row_str = str(buf_row)
            num_spaces = (max((len(str(len(buf)))), len(str(R))) - len(row_str))
            line_num_str = " " * num_spaces + row_str + "  |" 

            try:
                s.addstr(row, 0, line_num_str)
            except Exception as e:
                raise Exception("Failed to print: ", line_num_str, "Due to", e)
            for col in range(C):
                buf_col = col + x
                try:
                    s.addch(row, col + len(line_num_str) + 1, buf[buf_row][buf_col])
                except:
                    pass
            s.clrtoeol()
            try:
                s.addch('\n')
            except:
                pass

        s.addstr(R - 1, 0, editor_state)

        curses.curs_set(False)
        s.move(r-y, margin_l + c-x)
        s.refresh()
        curses.curs_set(True)

        while ch == -1:
            ch = s.getch()

        if ch == 27: 
            editor_state = "Normal"
            curses.curs_set(0)


        elif chr(ch) in '\n\r': # handle enter
            line = buf[r][c:]
            buf [r] = buf[r][:c]
            r += 1
            c = 0
            max_c = 0
            buf.insert(r, [] + line)

        elif ch == ord("w") and editor_state == "Normal":
            c = buf[r][c + 1:].index(ord(" ")) + c + 2 if ord(" ") in buf[r][c + 1:] else len(buf[r])
            max_c = c
        elif ch == ord("b") and editor_state == "Normal" and c > 0:
            c = c - buf[r][:c-1][::-1].index(ord(" ")) - 1 if ord(" ") in buf[r][:c - 1] else 0
            max_c = c

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
        
curses.wrapper(main)
