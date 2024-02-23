from Token import Token
class UParser:
    def __init__(self, tokens):
        self.currentToken = 0
        self.tokens = tokens
    
    def RULE_PROGRAM(self):
        if self.tokens[self.currentToken] == "{": self.currentToken += 1
        else: exit()

        self.RULE_BODY()

        if self.tokens[self.currentToken] == "}": self.currentToken += 1
        else: exit()

    def RULE_BODY(self):
        self.RULE_EXPRESSION()
        
    def RULE_EXPRESSION(self):
        self.RULE_X()

        if self.tokens[self.currentToken] == "|": self.currentToken += 1

        self.RULE_X()

    def RULE_X(self):
        self.RULE_R()

        if self.tokens[self.currentToken] == "|": self.currentToken += 1

        self.RULE_R()

    def RULE_R(self):
        self.RULE_E()

    def RULE_E(self):
        self.RULE_A()

        if self.tokens[self.currentToken] == "-" or self.tokens[self.currentToken] == "+": self.currentToken += 1

        self.RULE_A()

    def RULE_A(self):
        self.RULE_B()

        if self.tokens[self.currentToken] == "/" or self.tokens[self.currentToken] == "*": self.currentToken += 1

        self.RULE_B()

    def RULE_B(self):
        if self.tokens[self.currentToken] == "-": self.currentToken += 1
        else: exit()

        self.RULE_C()

    def RULE_C(self):
        if self.tokens[self.currentToken].getToken() == "INTEGER":
            self.currentToken += 1

        if self.tokens[self.currentToken].getToken() == "ID":
            self.currentToken += 1

        else:
            if self.tokens[self.currentToken] == "(": self.currentToken += 1
            else: exit()

            self.RULE_EXPRESSION()

            if self.tokens[self.currentToken] == ")": self.currentToken += 1
            else: exit()




