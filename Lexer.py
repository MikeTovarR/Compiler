from Token import Token
class Lexer:
    
    KEYWORDS = ("if", "else", "while", "switch", "case", "return", 
                "int", "float", "void", "char", "string", "boolean", 
                "true", "false", "print")
    
    # Constants
    ZERO = 0
    PESO = 1
    _ = 2
    ONE = 3
    _2_7 = 4
    _8_9 = 5
    A = 6
    B = 7
    C_D = 8
    E = 9
    F = 10
    G_W = 11
    X = 12
    Y_Z = 13
    DOT = 14
    DQM = 15
    QM = 16
    MINUS = 17
    PLUS = 18
    AT = 19
    OTHER = 20
    DELIMITER = 21

    ERROR = 23
    STOP = -2

    # states table; THIS IS THE TABLE FOR BINARY NUMBERS;
    stateTable = [
        [1, 4, 4, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 3, 18, 20, STOP, STOP, ERROR, ERROR, STOP],
        [6, ERROR, ERROR, 6, 6, ERROR, ERROR, 5, ERROR, 15, 14, ERROR, 7, ERROR, 8, STOP, STOP, STOP, STOP, ERROR, ERROR, STOP],
        [9, ERROR, ERROR, 9, 9, 9, ERROR, ERROR, ERROR, 15, 14, ERROR, ERROR, ERROR, 8, STOP, STOP, STOP, STOP, ERROR, ERROR, STOP],
        [10, ERROR, ERROR, 10, 10, 10, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, STOP, STOP, STOP, STOP, ERROR, ERROR, STOP],
        [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, ERROR, STOP, STOP, STOP, STOP, ERROR, ERROR, STOP],
        [12, ERROR, ERROR, 12, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, STOP, STOP, STOP, STOP, ERROR, ERROR, STOP],
        [6, ERROR, ERROR, 6, 6, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, STOP, STOP, STOP, STOP, ERROR, ERROR, STOP],
        [13, ERROR, ERROR, 13, 13, 13, 13, 13, 13, 13, 13, ERROR, ERROR, ERROR, ERROR, STOP, STOP, STOP, STOP, ERROR, ERROR, STOP],
        [10, ERROR, ERROR, 10, 10, 10, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, STOP, STOP, STOP, STOP, ERROR, ERROR, STOP],
        [9, ERROR, ERROR, 9, 9, 9, ERROR, ERROR, ERROR, 15, 14, ERROR, ERROR, ERROR, 8, STOP, STOP, STOP, STOP, ERROR, ERROR, STOP],
        [10, ERROR, ERROR, 10, 10, 10, ERROR, ERROR, ERROR, 15, 14, ERROR, ERROR, ERROR, ERROR, STOP, STOP, STOP, STOP, ERROR, ERROR, STOP],
        [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, ERROR, STOP, STOP, STOP, STOP, ERROR, ERROR, STOP],
        [12, ERROR, ERROR, 12, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, STOP, STOP, STOP, STOP, ERROR, ERROR, STOP],
        [13, ERROR, ERROR, 13, 13, 13, 13, 13, 13, 13, 13, ERROR, ERROR, ERROR, ERROR, STOP, STOP, STOP, STOP, ERROR, ERROR, STOP],
        [ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, STOP, STOP, STOP, STOP, ERROR, ERROR, STOP],
        [ERROR, ERROR, ERROR, 17, 17, 17, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, STOP, STOP, 16, 16, ERROR, ERROR, STOP],
        [ERROR, ERROR, ERROR, 17, 17, 17, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, STOP, STOP, STOP, STOP, ERROR, ERROR, STOP],
        [17, ERROR, ERROR, 17, 17, 17, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, STOP, STOP, STOP, STOP, ERROR, ERROR, STOP],
        [18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 19, 18, 18, 18, 18, ERROR, 18],
        #[ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, 20, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR],
        [STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, ERROR, STOP],
        [21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, ERROR, ERROR, 21, 21, 21, ERROR, 21],
        [ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, 22, ERROR, ERROR, ERROR, ERROR, ERROR],
        [STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, STOP, ERROR, STOP],
        [ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, STOP, STOP, STOP, STOP, ERROR, ERROR, STOP]
    ]

    def __init__(self, text):
        self.text = text
        self.tokens = []

    # run
    def run(self):
        lines = self.text.splitlines()
        for row, line in enumerate(lines, 1):
            self.split_line(row, line)

    # split lines
    def split_line(self, row, line):
        state = 0
        last_state = 0
        index = 0
        current_char = ''
        string = ''
        if not line:
            return

        # DFA working
        while index < len(line) and state != self.STOP:
            current_char = line[index]
            last_state = state
            state = self.calculate_next_state(state, current_char)
            if state != self.STOP:
                string += current_char
                index += 1
        if state == -2: state = last_state

        # review final state
        if state in (4, 11):
            if self.is_keyword(string):
                self.tokens.append(Token(string, "KEYWORD", row))
            else: 
                self.tokens.append(Token(string, "ID", row))
        elif state == 6:
            self.tokens.append(Token(string, "OCTAL", row))
        elif state in (1, 2, 9):
            self.tokens.append(Token(string, "INTEGER", row))
        elif state in (8, 10, 14, 17):
            self.tokens.append(Token(string, "FLOAT", row))
        elif state == 12:
            self.tokens.append(Token(string, "BINARY", row))
        elif state == 13:
            self.tokens.append(Token(string, "HEX", row))
        elif state == 19:
            self.tokens.append(Token(string, "STRING", row))
        elif state == 22:
            self.tokens.append(Token(string, "CHAR", row))
        elif state in (18, 20, 21, 23):
            self.tokens.append(Token(string, "ERROR", row))
        elif self.is_delimiter(current_char):
            self.tokens.append(Token(current_char, "DELIMITER", row))
            index += 1
        elif self.is_space(current_char):
            index += 1
        elif self.is_operator(current_char) or current_char in ('+', '-'):
            self.tokens.append(Token(current_char, "OPERATOR", row))
            index += 1
        else:
            if string.strip():
                self.tokens.append(Token(string, "ERROR", row))        

        # loop
        if index < len(line):
            self.split_line(row, line[index:])

    # calculate state
    def calculate_next_state(self, state, current_char):
        if self.is_delimiter(current_char) or self.is_operator(current_char) or self.is_space(current_char):
            return self.stateTable[state][self.DELIMITER]
        elif current_char == '0':
            return self.stateTable[state][self.ZERO]
        elif current_char == '$':
            return self.stateTable[state][self.PESO]
        elif current_char == '_':
            return self.stateTable[state][self._]
        elif current_char == '1':
            return self.stateTable[state][self.ONE]
        elif current_char in ('2', '3', '4', '5', '6', '7'):
            return self.stateTable[state][self._2_7]
        elif current_char in ('8', '9'):
            return self.stateTable[state][self._8_9]
        elif current_char == 'a' or current_char == 'A':
            return self.stateTable[state][self.A]
        elif current_char == 'b' or current_char == 'B':
            return self.stateTable[state][self.B]
        elif current_char in ['c', 'C', 'd', 'D']:
            return self.stateTable[state][self.C_D]
        elif current_char == 'e' or current_char == 'E':
            return self.stateTable[state][self.E]
        elif current_char == 'f' or current_char == 'F':
            return self.stateTable[state][self.F]
        elif current_char in ('g', 'G', 'h', 'H', 'i', 'I', 'j', 'J', 'k', 'K', 'l', 'L', 
                              'm', 'M', 'n', 'N', 'o', 'O', 'p', 'P', 'q', 'Q', 'r', 'R', 
                              's', 'S', 't', 'T', 'u', 'U', 'v', 'V', 'w', 'W'):
            return self.stateTable[state][self.G_W]
        elif current_char == 'x' or current_char == 'X':
            return self.stateTable[state][self.X]
        elif current_char in ['y', 'Y', 'z', 'Z']:
            return self.stateTable[state][self.Y_Z]
        elif current_char == '.':
            return self.stateTable[state][self.DOT]
        elif current_char == '"':
            return self.stateTable[state][self.DQM]
        elif current_char == '\'':
            return self.stateTable[state][self.QM]
        elif current_char == '-':
            return self.stateTable[state][self.MINUS]
        elif current_char == '+':
            return self.stateTable[state][self.PLUS]
        elif current_char == '@':
            return self.stateTable[state][self.AT]
        return self.stateTable[state][self.OTHER]

    # isDelimiter
    def is_delimiter(self, c):
        delimiters = (':', ';', '}', '{', '[', ']', '(', ')', ',')
        return c in delimiters

    # isOperator
    def is_operator(self, o):
        operators = ('*', '/', '<', '>', '=', '!', '&', '|', '%')
        return o in operators

    # isSpace
    def is_space(self, o):
        return o == ' '
    
    # isKeyword
    def is_keyword(self, o):
        return o in self.KEYWORDS

    # getTokens
    def get_tokens(self):
        return self.tokens