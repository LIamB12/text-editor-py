import curses
import sys
from text_buffer import TextBuffer

class EditSession:
    
    def __init__(self, filename):

        #initialize screen
        screen = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

        screen.nodelay(True)
        curses.noecho()
        curses.raw()
        curses.set_escdelay(1)
        screen.keypad(True)
        R, C = screen.getmaxyx() 

        #initialze buffer
        buffer = TextBuffer(filename)

        self.buffer_list = [buffer]
        self.screen = screen
        self.current_buffer = 0
        self.current_screen = 0
        self.ROW_NUM = R
        self.COL_NUM = C

    def get_current_buffer(self):
        return self.buffer_list[self.current_buffer]

    def scroll_buffer(self):
        buf = self.get_current_buffer()
        if buf.row < buf.cursor_y:
            buf.cursor_y = buf.row

        if buf.row >= buf.cursor_y + self.ROW_NUM - 2:
            buf.cursor_y = buf.row - self.ROW_NUM + 3

        if buf.col < buf.cursor_x:
            buf.cursor_x = buf.col

        if buf.col >= buf.cursor_x + self.COL_NUM:
            buf.cursor_x = buf.col - self.COL_NUM + 1

    def print_screen(self):
        buf = self.get_current_buffer()
        color_map = buf.parse_buffer()

        for row in range(self.ROW_NUM - 2):
            buf_row = row + buf.cursor_y

            row_str = str(buf_row)
            num_spaces = (max((len(str(len(buf.buf)))), len(str(self.ROW_NUM))) - len(row_str))
            line_num_str = " " * num_spaces + row_str + "  |" 

            self.screen.addstr(row, 0, line_num_str)
            for col in range(self.COL_NUM):
                buf_col = col + buf.cursor_x
                try:
                    color = color_map.get((buf_row, buf_col), 0)

                    self.screen.addch(row, col + len(line_num_str) + 1, buf.buf[buf_row][buf_col], curses.color_pair(color))
                except:
                    pass
            self.screen.clrtoeol()
            try:
                self.screen.addch('\n')
            except:
                pass

        self.screen.addstr(self.ROW_NUM - 1, 0, buf.state)

    def update_cursor(self):
        buf = self.get_current_buffer()

        row = buf.buf[buf.row] if buf.row < len(buf.buf) else None
        row_len = len(row) if row is not None else 0
        if buf.col > row_len:
            buf.col = row_len

        curses.curs_set(False)
        self.screen.move(buf.row-buf.cursor_y, self.get_left_margin() + buf.col-buf.cursor_x)
        self.screen.refresh()
        curses.curs_set(True)

    def get_left_margin(self):
        buf = self.get_current_buffer()
        return max(len(str(len(buf.buf))), len(str(self.ROW_NUM))) + 4

    

    def handle_key_press(self, key):
        buf = self.get_current_buffer()
        mode = buf.state

        if mode == "Insert":
            self._handle_insert_mode_key_press(key)
        if mode == "Normal":
            self._handle_normal_mode_key_press(key)


    def _handle_insert_mode_key_press(self, key):
        buf = self.get_current_buffer()

        if chr(key) in '\n\r': # handle enter
            line = buf.buf[buf.row][buf.col:]

            buf.buf[buf.row] = buf.buf[buf.row][:buf.col]
            buf.row += 1
            buf.col = 0
            buf.jump_to_col = 0

            buf.buf.insert(buf.row, [] + line)

        elif key == 27: # Esc
            buf = self.get_current_buffer()
            buf.state = "Normal"

        
        elif key == (ord("q") & 0x1f): #Ctrl-Q quits
            sys.exit()


        elif key != (key & 0x1f) and key < 128:
            buf.buf[buf.row].insert(buf.col, key)
            buf.col += 1
            buf.jump_to_col += 1


        elif key in [8, 263]: # Backspace
            if buf.col > 0:
                buf.col -= 1
                buf.jump_to_col -= 1
                del buf.buf[buf.row][buf.col]
            elif buf.row > 0:
                line = buf.buf[buf.row]
                del buf.buf[buf.row]
                buf.row -= 1
                prev_line_len = len(buf.buf[buf.row])
                buf.buf[buf.row] += line
                buf.col = prev_line_len
                buf.jump_to_col = prev_line_len



        

    def _handle_normal_mode_key_press(self, key):
        buf = self.get_current_buffer()

        if key == (ord("q") & 0x1f): #Ctrl-Q quits
            sys.exit()

        elif key == ord("i"): 
            buf.state = "Insert"
        
        elif key == curses.KEY_RIGHT or key == ord('l'):
            if buf.col < len(buf.buf[buf.row]):
                buf.col += 1
                buf.jump_to_col += 1
            elif buf.row < len(buf.buf) - 1:
                buf.row += 1
                buf.col = 0
                buf.jump_to_col = 0

        elif key == curses.KEY_LEFT or key == ord('h'):
            if buf.col > 0:
                buf.col -= 1
                buf.jump_to_col -= 1
            elif buf.row > 0:
                buf.row -= 1
                buf.col = len(buf.buf[buf.row])
                buf.jump_to_col = len(buf.buf[buf.row])

        elif (key == curses.KEY_UP or key == ord("k")) and buf.row != 0:
            buf.row -= 1
            buf.col = buf.jump_to_col

        elif (key == curses.KEY_DOWN or key == ord("j")) and buf.row < len(buf.buf):
            buf.row += 1
            buf.col = buf.jump_to_col


