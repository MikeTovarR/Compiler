from Token import Token
class UParser:
    def __init__(self, tokens):
        self.currentToken = 0
        self.tokens = tokens

    def exitParser(self, error, line, word):
        isIncremented = False
        print(f"ERROR {error}")
        if error == 1: print("Line  "+str(line)+": invalid \""+str(word)+"\" expected {")
        elif error == 2: print("Line  "+str(line)+": invalid \""+str(word)+"\" expected }")
        elif error == 3: print("Line  "+str(line)+": invalid \""+str(word)+"\" expected ;")
        elif error == 4: 
            print("Line  "+str(line)+": invalid \""+str(word)+"\" expected IDENTIFIER or KEYWORD")
            isIncremented = True
        elif error == 5: print("Line  "+str(line)+": invalid \""+str(word)+"\" expected =")
        elif error == 6: print("Line  "+str(line)+": invalid \""+str(word)+"\" expected IDENTIFIER")
        elif error == 7: print("Line  "+str(line)+": invalid \""+str(word)+"\" expected (")
        elif error == 8: print("Line  "+str(line)+": invalid \""+str(word)+"\" expected )")
        elif error == 9: print("Line  "+str(line)+": invalid \""+str(word)+"\" expected COMPARATOR")
        elif error == 10: 
            print("Line  "+str(line)+": invalid \""+str(word)+"\" expected VALUE")
            isIncremented = True

        if isIncremented: self.currentToken += 1

    def RULE_PROGRAM(self):
        if self.tokens[self.currentToken].get_word() == "{": self.currentToken += 1
        else: self.exitParser(1, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

        self.RULE_BODY()

        if self.tokens[self.currentToken].get_word() == "}": self.currentToken += 1
        else: self.exitParser(2, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

    def RULE_BODY(self):
        while self.tokens[self.currentToken].get_word() != "}": 
            if self.tokens[self.currentToken].get_token() == "ID":
                self.RULE_ASSIGMENT()
                if self.tokens[self.currentToken].get_word() == ";": self.currentToken += 1
                else: self.exitParser(3, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())
            #Incluir todos los tipos de variable
            elif self.tokens[self.currentToken].get_word() == "int":
                self.RULE_VARIABLE()
                if self.tokens[self.currentToken].get_word() == ";": self.currentToken += 1
                else: self.exitParser(3, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())
            elif self.tokens[self.currentToken].get_word() == "while":
                self.RULE_WHILE()
            elif self.tokens[self.currentToken].get_word() == "if":
                self.RULE_IF()
            elif self.tokens[self.currentToken].get_word() == "print":
                self.RULE_PRINT()
                if self.tokens[self.currentToken].get_word() == ";": self.currentToken += 1
                else: self.exitParser(3, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())
            elif self.tokens[self.currentToken].get_word() == "return":
                self.RULE_RETURN()
                if self.tokens[self.currentToken].get_word() == ";": self.currentToken += 1
                else: self.exitParser(3, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())
            else: self.exitParser(4, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

            """
            if self.currentToken >= len(self.tokens): 
                self.currentToken -= 1
                break
            """

    def RULE_ASSIGMENT(self):
        self.currentToken += 1

        if self.tokens[self.currentToken].get_word() == "=": self.currentToken += 1  
        else: self.exitParser(5, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

        self.RULE_EXPRESSION()

    def RULE_VARIABLE(self):
        self.currentToken += 1

        if self.tokens[self.currentToken].get_token() == "ID": self.currentToken += 1
        else: self.exitParser(6, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())
            
    def RULE_WHILE(self):
        self.currentToken += 1

        if self.tokens[self.currentToken].get_word() == "(": self.currentToken += 1
        else: self.exitParser(7, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

        self.RULE_EXPRESSION()

        if self.tokens[self.currentToken].get_word() == ")": self.currentToken += 1
        else: self.exitParser(8, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

        self.RULE_PROGRAM()

    def RULE_IF(self):
        self.currentToken += 1

        if self.tokens[self.currentToken].get_word() == "(": self.currentToken += 1
        else: self.exitParser(7, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

        self.RULE_EXPRESSION()

        if self.tokens[self.currentToken].get_word() == ")": self.currentToken += 1
        else: self.exitParser(8, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

        self.RULE_PROGRAM()

        if self.tokens[self.currentToken].get_word() == "else": 
            self.currentToken += 1
            self.RULE_PROGRAM()

    def RULE_RETURN(self):
        self.currentToken += 1

    def RULE_PRINT(self):
        self.currentToken += 1

        if self.tokens[self.currentToken].get_word() == "(": self.currentToken += 1
        else: self.exitParser(7, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

        self.RULE_EXPRESSION()

        if self.tokens[self.currentToken].get_word() == ")": self.currentToken += 1
        else: self.exitParser(8, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

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
            elif self.tokens[self.currentToken].get_word() == "=":  self.exitParser(9, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())
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
        if self.tokens[self.currentToken].get_token() in {"INTEGER", "OCTAL", "HEX", "BINARY", "STRING", "CHAR", "FLOAT", "ID"}:
            self.currentToken += 1
        if self.tokens[self.currentToken].get_word() in {"true", "false"}:
            self.currentToken += 1
        elif self.tokens[self.currentToken].get_word() == "(": 
            self.currentToken += 1
            self.RULE_EXPRESSION()

            if self.tokens[self.currentToken].get_word() == ")": self.currentToken += 1
            else: self.exitParser(8, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())
        else: self.exitParser(10, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())




