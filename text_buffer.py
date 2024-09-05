from tree_sitter import Language, Parser
import tree_sitter_python as tspython
import os

PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)

string_node_types = ["integer", "string_content", "string_start", "string_end"]
keyword_node_types = ["import", "def", "for", "if", "else", "elif", "as", "while", "try", "with", "except", "pass", "raise", "class", "from", "return"]
comment_node_types = ["comment"]
operation_node_types = ["in", "and", "or", ",", ".","=", ">", "<", "/", "[", "]", "}", "{", "(", ")", "*", "+", "-", "/", ":", "==", "!=", ">=", "<=", "+=", "-=", "*=", "/=", "&", "|"]

word_chars = [97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 95]
separators = [59, 58, 42, 94, 38, 37, 36, 35, 64, 33, 43, 61, 45, 96, 126, 92, 44, 46, 47, 63, 62, 60, 61, 40, 41, 123, 125, 91, 93, 39, 34]


class TextBuffer:

    def __init__(self, buffer, filename, initial_state):
        self.buf = buffer
        self.filename = filename
        self.state = initial_state
        self.cursor_x, self.cursor_y, self.row, self.col, self.jump_to_col = 0, 0, 0, 0, 0
        self.colors = {}

    @staticmethod 
    def buffer_from_file(file):
        buf = []
        try:
            with open(file) as f:
                content = f.read().split('\n')
                content = content[:-1] if len(content) > 1 else content
                for row in content:
                    buf.append([ord(c) for c in row])
        except:
            buf.append([])
        return TextBuffer(buf, file, "Normal")

    @staticmethod 
    def create_netrw_buffer(path):
        buf = []
        try:
            for file in os.listdir(path):
                buf.append([ord(c) for c in file])
        except:
            buf.append([])
        return TextBuffer(buf, path, "Netrw")

    def get_last_word_col(self):

        if self.col == 0:
            if self.row > 0:
                self.row -= 1
                return len(self.buf[self.row]) - 1 if len(self.buf[self.row]) - 1 > 0 else 0

            else:
                return self.col

        if self.buf[self.row] == []:
            self.row -= 1
            return len(self.buf[self.row]) - 1
    

        found_non_word_char = self.buf[self.row][self.col] in separators or self.buf[self.row][self.col] not in word_chars
        for index in range(self.col - 1, 0, -1):
            char = self.buf[self.row][index]
            if found_non_word_char:
                if char in separators or char in word_chars:
                    return index
            elif char in separators:
                return index
            elif char not in word_chars:
                found_non_word_char = True
        
        
        if self.row == 0:
            return self.col
        else:
            self.row -= 1
            return len(self.buf[self.row]) - 1 if len(self.buf[self.row]) - 1 > 0 else 0


    def get_next_word_col(self):

        if self.col == len(self.buf[self.row]):
            if self.row < len(self.buf) - 1:
                self.row += 1
                return 0
            else:
                return self.col

        if self.buf[self.row] == []:
            self.row += 1
            return 0
    

        found_non_word_char = self.buf[self.row][self.col] in separators or self.buf[self.row][self.col] not in word_chars
        for index in range(self.col + 1, len(self.buf[self.row])):
            char = self.buf[self.row][index]
            if found_non_word_char:
                if char in separators or char in word_chars:
                    return index
            elif char in separators:
                return index
            elif char not in word_chars:
                found_non_word_char = True
        
        
        if self.row == len(self.buf) - 1:
            return self.col
        else:
            self.row += 1
            return 0

    def parse_buffer(self):
        color_map = {}
        tree = parser.parse(self.to_bytes())
    
        for node in TextBuffer._traverse_tree(tree):
            if node.type == "function_definition":
                for child in node.children:
                    if child.type == "identifier":
                        for i in range(child.start_point.column, child.end_point.column):
                            color_map[(child.start_point.row, i)] = 5
                        

            if node.type == "call":
                for child in node.children:
                    if child.type == "identifier":
                        for i in range(child.start_point.column, child.end_point.column):
                            color_map[(child.start_point.row, i)] = 5
                    elif child.type == "attribute":
                        for child2 in child.children:

                            if child2.type == ".":
                                func_identifier_node = child2.next_sibling
                                for i in range(func_identifier_node.start_point.column, func_identifier_node.end_point.column):
                                    color_map[(func_identifier_node.start_point.row, i)] = 6
                        
            elif node.type == "." and node.parent.parent.type != "call":
                property_identifier_node = node.next_sibling
                if not property_identifier_node:
                    continue

                for i in range(property_identifier_node.start_point.column, property_identifier_node.end_point.column):
                    color_map[(property_identifier_node.start_point.row, i)] = 11
            
            
            elif (len(node.children) == 0):

                token = self.buf[node.start_point.row][node.start_point.column:node.end_point.column]
                token = "".join([chr(x) for x in token])

                if node.type in string_node_types:

                    for i in range(node.start_point.column, node.end_point.column):
                        color_map[(node.start_point.row, i)] = 1

                elif node.type in keyword_node_types:
                    for i in range(node.start_point.column, node.end_point.column):
                        color_map[(node.start_point.row, i)] = 4

                elif node.type in comment_node_types:
                    for i in range(node.start_point.column, node.end_point.column):
                        color_map[(node.start_point.row, i)] = 9

                elif node.type in operation_node_types:
                    for i in range(node.start_point.column, node.end_point.column):
                        color_map[(node.start_point.row, i)] = 3
                
                elif token == token.upper():
                    for i in range(node.start_point.column, node.end_point.column):
                        color_map[(node.start_point.row, i)] = 1

                elif token[0] == token[0].upper():
                    for i in range(node.start_point.column, node.end_point.column):
                        color_map[(node.start_point.row, i)] = 11
                elif token == "self":
                    for i in range(node.start_point.column, node.end_point.column):
                        color_map[(node.start_point.row, i)] = 7
                
        return color_map

    @staticmethod
    def _traverse_tree(tree):
        cursor = tree.walk()

        visited_children = False
        while True:
            if not visited_children:
                yield cursor.node
                if not cursor.goto_first_child():
                    visited_children = True
            elif cursor.goto_next_sibling():
                visited_children = False
            elif not cursor.goto_parent():
                break        
        
    def to_bytes(self):
        buf_to_chars = []
        for row in self.buf:
            char_row = [chr(x) for x in row]
            buf_to_chars.append("".join(char_row))

        return bytes("\n".join(buf_to_chars), encoding="utf-8")

    def to_string(self):
        buf_to_chars = []
        for row in self.buf:
            char_row = [chr(x) for x in row]
            buf_to_chars.append("".join(char_row))

        return "\n".join(buf_to_chars)

    def to_line_array(self):
        buf_to_chars = []
        for row in self.buf:
            char_row = [chr(x) for x in row]
            buf_to_chars.append("".join(char_row))
        return buf_to_chars

