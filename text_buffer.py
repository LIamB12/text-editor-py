from tree_sitter import Language, Parser
import tree_sitter_python as tspython
import os

PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)
string_node_types = ["integer", "string_content", "string_start", "string_end"]
keyword_node_types = ["import", "def", "for", "if", "else", "elif", "as", "while", "try", "with", "except", "pass", "raise", "class", "from", "return"]
comment_node_types = ["comment"]
operation_node_types = ["in", "and", "or", ",", ".","=", ">", "<", "/", "[", "]", "}", "{", "(", ")", "*", "+", "-", "/", ":", "==", "!=", ">=", "<=", "+=", "-=", "*=", "/=", "&", "|"]

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

