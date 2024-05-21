from Token import Token

class UParser:
    def __init__(self, tokens):
        self.currentToken = 0
        self.tokens = tokens
        self.FIRST = dict()
        self.FOLLOW = dict()
        self.buildFandF()

    def buildFandF(self):
        self.FIRST["PROGRAM"] = {"{"}
        self.FIRST["PRINT"] = {"print"}
        self.FIRST["ASSIGMENT"] = {"ID"}
        self.FIRST["VARIABLE"] = {"int", "float", "bool", "void", "char", "string"}
        self.FIRST["RETURN"] = {"return"}
        self.FIRST["WHILE"] = {"while"},
        self.FIRST["IF"] = {"if"}
        self.FIRST["RETURN"] = {"return"}
        self.FIRST["BODY"] = self.FIRST["PRINT"].union(self.FIRST["ASSIGMENT"].union(self.FIRST["VARIABLE"].union(self.FIRST["WHILE"].union(self.FIRST["IF"].union(self.FIRST["RETURN"])))))
        self.FIRST["C"] = {"INTEGER", "OCTAL", "HEX", "BINARY", "true", "false", "STRING", "CHAR", "FLOAT", "ID", "("}
        self.FIRST["B"] = {"-"}.union(self.FIRST["C"])
        self.FIRST["A"] = self.FIRST["B"]
        self.FIRST["E"] = self.FIRST["A"]
        self.FIRST["R"] = self.FIRST["E"]
        self.FIRST["Y"] = {"!"}.union(self.FIRST["R"])
        self.FIRST["X"] = self.FIRST["Y"]
        self.FIRST["EXPRESSION"] = self.FIRST["X"]

        self.FOLLOW["PROGRAM"] = {"EOF"}
        self.FOLLOW["PRINT"] = {";"}
        self.FOLLOW["ASSIGMENT"] = {";"}
        self.FOLLOW["VARIABLE"] = {";"}
        self.FOLLOW["RETURN"] = {";"}]
        self.FOLLOW["BODY"] = {";"}
        self.FOLLOW["WHILE"] = {"}"}.union(self.FIRST["BODY"])
        self.FOLLOW["IF"] = {"}"}.union(self.FIRST["BODY"])
        self.FOLLOW["RETURN"] = {"}"}.union(self.FIRST["BODY"])
        self.FOLLOW["EXPRESSION"] = {")", ";"}
        self.FOLLOW["X"] = {"|"}.union(self.FOLLOW["EXPRESSION"])
        self.FOLLOW["Y"] = {"&"}.union(self.FOLLOW["X"])
        self.FOLLOW["R"] = self.FOLLOW["Y"]
        self.FOLLOW["E"] = {"!=", "==", ">", "<"}.union(self.FOLLOW["R"])
        self.FOLLOW["A"] =  {"-", "+"}.union(self.FOLLOW["E"])
        self.FOLLOW["B"] = {"*", "/"}.union(self.FOLLOW["A"])
        self.FOLLOW["C"] = self.FOLLOW["B"]

    def incrementToken(self):
        # print(f"{self.currentToken}, {len(self.tokens)}")
        if self.currentToken < len(self.tokens) - 1:
            self.currentToken += 1

    def exitParser(self, error, line, word):
        isIncremented = False
        print(f"ERROR {error}")
        if error == 1: print("Line  "+str(line)+": invalid \""+str(word)+"\" expected {")
        elif error == 2: print("Line  "+str(line)+": invalid \""+str(word)+"\" expected }")
        elif error == 3: 
            print("Line  "+str(line)+": invalid \""+str(word)+"\" expected ;")
        elif error == 4: 
            print("Line  "+str(line)+": invalid \""+str(word)+"\" expected IDENTIFIER or KEYWORD")
            isIncremented = True
        elif error == 5: print("Line  "+str(line)+": invalid \""+str(word)+"\" expected =")
        elif error == 6: print("Line  "+str(line)+": invalid \""+str(word)+"\" expected IDENTIFIER")
        elif error == 7: print("Line  "+str(line)+": invalid \""+str(word)+"\" expected (")
        elif error == 8: print("Line  "+str(line)+": invalid \""+str(word)+"\" expected )")
        elif error == 9: print("Line  "+str(line)+": invalid \""+str(word)+"\" expected COMPARATOR")
        elif error == 10: 
            print("Line  "+str(line)+": invalid \""+str(word)+"\" expected VALUE, IDENTIFIER or (")
            isIncremented = True

        if isIncremented: self.incrementToken()

    def RULE_PROGRAM(self):
        if self.tokens[self.currentToken].get_word() == "{": self.incrementToken()
        else: self.exitParser(1, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

        while not (self.tokens[self.currentToken].get_word() in self.FIRST["BODY"] or self.tokens[self.currentToken].get_token() in self.FIRST["BODY"] or self.tokens[self.currentToken].get_word() == "}"):
            self.incrementToken()

        self.RULE_BODY()

        if self.tokens[self.currentToken].get_word() == "}": self.incrementToken()
        else: self.exitParser(2, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

    def RULE_BODY(self):
        while self.tokens[self.currentToken].get_word() != "}": 
            if self.tokens[self.currentToken].get_token() == "ID":
                self.RULE_ASSIGMENT()
                if self.tokens[self.currentToken].get_word() == ";": self.incrementToken()
                else: self.exitParser(3, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())
            #Incluir todos los tipos de variable
            elif self.tokens[self.currentToken].get_word() == "int" or self.tokens[self.currentToken].get_word() == "float" or self.tokens[self.currentToken].get_word() == "bool" or self.tokens[self.currentToken].get_word() == "char" or self.tokens[self.currentToken].get_word() == "string" or self.tokens[self.currentToken].get_word() == "void":
                self.RULE_VARIABLE()
                if self.tokens[self.currentToken].get_word() == ";": self.incrementToken()
                else: self.exitParser(3, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())
            elif self.tokens[self.currentToken].get_word() == "while":
                self.RULE_WHILE()
            elif self.tokens[self.currentToken].get_word() == "if":
                self.RULE_IF()
            elif self.tokens[self.currentToken].get_word() == "print":
                self.RULE_PRINT()
                if self.tokens[self.currentToken].get_word() == ";": self.incrementToken()
                else: self.exitParser(3, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())
            elif self.tokens[self.currentToken].get_word() == "return":
                self.RULE_RETURN()
                if self.tokens[self.currentToken].get_word() == ";": self.incrementToken()
                else: self.exitParser(3, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())
            else: self.exitParser(4, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

            if self.currentToken == len(self.tokens) - 1:
                break

            while not (self.tokens[self.currentToken].get_word() in self.FIRST["BODY"] or self.tokens[self.currentToken].get_token() in self.FIRST["BODY"] or self.tokens[self.currentToken].get_word() in self.FOLLOW["BODY"]):
                self.incrementToken()

    def RULE_ASSIGMENT(self):
        self.incrementToken()

        if self.tokens[self.currentToken].get_word() == "=": 
            self.incrementToken()  
            self.RULE_EXPRESSION()
        else: self.exitParser(5, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())

        while not (self.tokens[self.currentToken].get_word() in self.FIRST["EXPRESSION"] or self.tokens[self.currentToken].get_token() in self.FIRST["EXPRESSION"] or self.tokens[self.currentToken].get_word() in self.FOLLOW["EXPRESSION"]):
                self.incrementToken()        

    def RULE_VARIABLE(self):
        self.incrementToken()
    
        if self.tokens[self.currentToken].get_token() == "ID": self.incrementToken()
        else: self.exitParser(6, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())
            
    def RULE_WHILE(self):
        self.incrementToken()

        if self.tokens[self.currentToken].get_word() == "(": self.incrementToken()
        else: self.exitParser(7, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())

        while not (self.tokens[self.currentToken].get_word() in self.FIRST["EXPRESSION"] or self.tokens[self.currentToken].get_token() in self.FIRST["EXPRESSION"] or self.tokens[self.currentToken].get_word() == ")"):
            self.incrementToken() 

        self.RULE_EXPRESSION()

        if self.tokens[self.currentToken].get_word() == ")": self.incrementToken()
        else: self.exitParser(8, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())

        while not (self.tokens[self.currentToken].get_word() in self.FIRST["PROGRAM"] or self.tokens[self.currentToken].get_token() in self.FIRST["PROGRAM"] or self.tokens[self.currentToken].get_word() in self.FOLLOW["PROGRAM"] or self.tokens[self.currentToken].get_token() in self.FOLOW["PROGRAM"]):
            self.incrementToken() 

        self.RULE_PROGRAM()

    def RULE_IF(self):
        self.incrementToken()

        if self.tokens[self.currentToken].get_word() == "(": self.incrementToken()
        else: self.exitParser(7, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())

        while not (self.tokens[self.currentToken].get_word() in self.FIRST["EXPRESSION"] or self.tokens[self.currentToken].get_token() in self.FIRST["EXPRESSION"] or self.tokens[self.currentToken].get_word() == ")"):
            self.incrementToken() 

        self.RULE_EXPRESSION()

        if self.tokens[self.currentToken].get_word() == ")": self.incrementToken()
        else: self.exitParser(8, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())

        while not (self.tokens[self.currentToken].get_word() in self.FIRST["PROGRAM"] or self.tokens[self.currentToken].get_token() in self.FIRST["PROGRAM"] or self.tokens[self.currentToken].get_word() in self.FOLLOW["PROGRAM"] or self.tokens[self.currentToken].get_token() in self.FOLOW["PROGRAM"]):
            self.incrementToken() 

        self.RULE_PROGRAM()

        if self.tokens[self.currentToken].get_word() == "else": 
            self.incrementToken()
            self.RULE_PROGRAM()

    def RULE_RETURN(self):
        self.incrementToken()

    def RULE_PRINT(self):
        self.incrementToken()

        if self.tokens[self.currentToken].get_word() == "(": 
            self.incrementToken()

            self.RULE_EXPRESSION()

            if self.tokens[self.currentToken].get_word() == ")": self.incrementToken()
            else: self.exitParser(8, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())
        else: self.exitParser(7, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())

        while not (self.tokens[self.currentToken].get_word() in self.FIRST["EXPRESSION"] or self.tokens[self.currentToken].get_token() in self.FIRST["EXPRESSION"] or self.tokens[self.currentToken].get_word() == ")"):
            self.incrementToken() 

    def RULE_EXPRESSION(self):
        self.RULE_X()

        if self.tokens[self.currentToken].get_word() == "|": 
            self.incrementToken()
            self.RULE_X()

    def RULE_X(self):
        self.RULE_Y()

        if self.tokens[self.currentToken].get_word() == "&": 
            self.incrementToken()
            self.RULE_Y()

    def RULE_Y(self):
        if self.tokens[self.currentToken].get_word() == "!": 
            if self.tokens[self.currentToken+1].get_word() == "=": 
                self.incrementToken()
                self.RULE_E()
            else: 
                self.incrementToken()
                self.RULE_R()
        else: self.RULE_R()

    def RULE_R(self):
        self.RULE_E()

        while self.tokens[self.currentToken].get_word() == "<" or self.tokens[self.currentToken].get_word() == ">" or self.tokens[self.currentToken].get_word() == "=":
            if self.tokens[self.currentToken+1].get_word() == "=":  
                self.incrementToken()
                self.incrementToken()
            elif self.tokens[self.currentToken].get_word() == "=":  self.exitParser(9, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())
            else: self.incrementToken()

            self.RULE_E()

    def RULE_E(self):
        self.RULE_A()

        if self.tokens[self.currentToken].get_word() == "-" or self.tokens[self.currentToken].get_word() == "+": 
            self.incrementToken()
            self.RULE_A()

    def RULE_A(self):
        self.RULE_B()

        if self.tokens[self.currentToken].get_word() == "/" or self.tokens[self.currentToken].get_word() == "*": 
            self.incrementToken()
            self.RULE_B()

    def RULE_B(self):
        if self.tokens[self.currentToken].get_word() == "-": self.incrementToken()

        self.RULE_C()

    def RULE_C(self):
        if self.tokens[self.currentToken].get_token() in {"INTEGER", "OCTAL", "HEX", "BINARY", "STRING", "CHAR", "FLOAT", "ID"}:
            self.incrementToken()
        elif self.tokens[self.currentToken].get_word() in {"true", "false"}:
            self.incrementToken()
        elif self.tokens[self.currentToken].get_word() == "(": 
            self.incrementToken()
            self.RULE_EXPRESSION()

            if self.tokens[self.currentToken].get_word() == ")": self.incrementToken()
            else: self.exitParser(8, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())
        else: self.exitParser(10, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())
