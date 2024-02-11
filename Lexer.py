class Lexer:
    
    KEYWORDS = ["if", "else", "while", "switch", "case", "return", 
                "int", "float", "void", "char", "string", "boolean", 
                "true", "false", "print"]
    ZERO = 1
    ONE = 2
    B = 0
    OTHER = 3
    DELIMITER = 4
    ERROR = 4
    STOP = -2

    stateTable = [
        [1, 4, 4, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 3, STOP],
        [6, ERROR, ERROR, 6, 6, ERROR, ERROR, 5, ERROR, 15, 14, ERROR, ERROR, ERROR, 8, STOP],
        [9, ERROR, ERROR, 9, 9, 9, ERROR, ERROR, ERROR, 15, 14, ERROR, ERROR, ERROR, 8, STOP],
        [10, ERROR, ERROR, 10, 10, 10, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, STOP],
        [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, STOP],
        [12, ERROR, ERROR, 12, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, STOP],
        [6, ERROR, ERROR, 6, 6, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, STOP],
        [13, ERROR, ERROR, 13, 13, 13, 13, 13, 13, 13, 13, ERROR, ERROR, ERROR, ERROR, STOP],
        [10, ERROR, ERROR, 10, 10, 10, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, STOP],
        [9, ERROR, ERROR, 9, 9, 9, ERROR, ERROR, ERROR, 15, 14, ERROR, ERROR, ERROR, 8, STOP],
        [10, ERROR, ERROR, 10, 10, 10, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, STOP],
        [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, ERROR, STOP],
        [12, ERROR, ERROR, 12, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, STOP],
        [13, ERROR, ERROR, 13, 13, 13, 13, 13, 13, 13, 13, ERROR, ERROR, ERROR, ERROR, STOP],
        [ERROR] * 16,
        [12, ERROR, ERROR, 12, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, STOP],
        [13, ERROR, ERROR, 13, 13, 13, 13, 13, 13, 13, 13, ERROR, ERROR, ERROR, ERROR, STOP],
        [ERROR] * 16,
        [ERROR] * 16,
        [ERROR] * 16,
        [17, ERROR, ERROR, 17, 17, 17, ERROR, ERROR, ERROR,    ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, 17],
    [ERROR] * 16,
    [17, ERROR, ERROR, 17, 17, 17, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, 17],
    [17, ERROR, ERROR, 17, 17, 17, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, STOP],
    [17, ERROR, ERROR, 17, 17, 17, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, STOP],
    [ERROR] * 16
]

def __init__(self, text):
    self.text = text

def run(self):
    self.tokens = []
    lines = self.text.splitlines()
    for row, line in enumerate(lines, 1):
        self.split_line(row, line)

def split_line(self, row, line):
    state = 0
    index = 0
    current_char = ''
    string = ''
    if not line:
        return

    while index < len(line) and state != self.STOP:
        current_char = line[index]
        state = self.calculate_next_state(state, current_char)
        if not self.is_delimiter(current_char) and not self.is_operator(current_char):
            string += current_char
        index += 1

    if state == 3:
        self.tokens.append(Token(string, "BINARY", row))
    else:
        if string.strip():
            self.tokens.append(Token(string, "ERROR", row))

    if self.is_delimiter(current_char):
        self.tokens.append(Token(current_char, "DELIMITER", row))
    elif self.is_operator(current_char):
        self.tokens.append(Token(current_char, "OPERATOR", row))

    if index < len(line):
        self.split_line(row, line[index:])

def calculate_next_state(self, state, current_char):
    if self.is_space(current_char) or self.is_delimiter(current_char) \
            or self.is_operator(current_char) or self.is_quotation_mark(current_char):
        return self.stateTable[state][self.DELIMITER]
    elif current_char == 'b':
        return self.stateTable[state][self.B]
    elif current_char == '0':
        return self.stateTable[state][self.ZERO]
    elif current_char == '1':
        return self.stateTable[state][self.ONE]
    return self.stateTable[state][self.OTHER]

def is_delimiter(self, c):
    delimiters = [':', ';', '}', '{', '[', ']', '(', ')', ',']
    return c in delimiters

def is_operator(self, o):
    operators = ['+', '-', '*', '/', '<', '>', '=', '!', '&', '|']
    return o in operators

def is_quotation_mark(self, o):
    quote = ['"', "'"]
    return o in quote

def is_space(self, o):
    return o == ' '

def get_tokens(self):
    return self.tokens

