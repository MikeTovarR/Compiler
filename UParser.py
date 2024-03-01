from Token import Token
class UParser:
    def __init__(self, tokens):
        self.currentToken = 0
        self.tokens = tokens
    
    def exitParser(self, error):
        print("ERROR ", error)
        exit()

    def RULE_PROGRAM(self):
        if self.tokens[self.currentToken].get_word() == "{": self.currentToken += 1
        else: self.exitParser(1)

        self.RULE_BODY()

        if self.tokens[self.currentToken].get_word() == "}": self.currentToken += 1
        else: self.exitParser(2)

    def RULE_BODY(self):
        while self.tokens[self.currentToken].get_word() != "}": 
            self.RULE_EXPRESSION()

            if self.tokens[self.currentToken].get_word() == ";": self.currentToken += 1
            else: self.exitParser(3)

    def RULE_EXPRESSION(self):
        self.RULE_X()

        while self.tokens[self.currentToken].get_word() == "|": 
            self.currentToken += 1
            self.RULE_X()

    def RULE_X(self):
        self.RULE_Y()

        while self.tokens[self.currentToken].get_word() == "&": 
            self.currentToken += 1
            self.RULE_Y()

    def RULE_Y(self):
        if self.tokens[self.currentToken].get_word() == "!": 
            if self.tokens[self.currentToken+1].get_word() == "=": 
                self.currentToken += 2
                self.RULE_E()
            else: 
                self.currentToken += 1
                self.RULE_R()
        else: self.RULE_R()

    def RULE_R(self):
        self.RULE_E()

        while self.tokens[self.currentToken].get_word() == "<" or self.tokens[self.currentToken].get_word() == ">" or self.tokens[self.currentToken].get_word() == "=":
            if self.tokens[self.currentToken+1].get_word() == "=":  self.currentToken += 2
            elif self.tokens[self.currentToken].get_word() == "=":  exit()
            else: self.currentToken += 1

            self.RULE_E()

    def RULE_E(self):
        self.RULE_A()

        if self.tokens[self.currentToken].get_word() == "-" or self.tokens[self.currentToken].get_word() == "+": 
            self.currentToken += 1
            self.RULE_A()

    def RULE_A(self):
        self.RULE_B()

        if self.tokens[self.currentToken].get_word() == "/" or self.tokens[self.currentToken].get_word() == "*": 
            self.currentToken += 1
            self.RULE_B()

    def RULE_B(self):
        if self.tokens[self.currentToken].get_word() == "-": self.currentToken += 1

        self.RULE_C()

    def RULE_C(self):
        if self.tokens[self.currentToken].get_token() == "INTEGER":
            self.currentToken += 1
        elif self.tokens[self.currentToken].get_token() == "ID":
            self.currentToken += 1
        elif self.tokens[self.currentToken].get_word() == "(": 
            self.currentToken += 1
            self.RULE_EXPRESSION()

            if self.tokens[self.currentToken].get_word() == ")": self.currentToken += 1
            else: self.exitParser(4)
        else: self.exitParser(5)




