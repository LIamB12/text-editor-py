#!/bin/python3

import curses, sys
from edit_session import EditSession

def main(stdscr):

    
    if len(sys.argv) == 2:
        src_file = sys.argv[1]
    else:
        print("Usage: python3 main3.py <filename>")
        return

    session = EditSession(src_file)

    while True:
        ch = -1

        session.scroll_buffer()
        session.print_screen()
        session.update_cursor()

        while ch == -1:
            ch = session.screen.getch()

        session.handle_key_press(ch)

curses.wrapper(main)
