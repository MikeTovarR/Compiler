from Token import Token

class UParser:
    def __init__(self, tokens):
        self.currentToken = 0
        self.tokens = tokens
        self.syntax_tree = {}

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
        self.syntax_tree = {"PROGRAM": {}}
        if self.tokens[self.currentToken].get_word() == "{": self.currentToken += 1
        else: self.exitParser(1, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

        self.RULE_BODY(self.syntax_tree["PROGRAM"])

        if self.tokens[self.currentToken].get_word() == "}": self.currentToken += 1
        else: self.exitParser(2, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

    def RULE_BODY(self, parent):
        while self.tokens[self.currentToken].get_word() != "}": 
            if self.tokens[self.currentToken].get_token() == "ID":
                assignment = {}
                self.RULE_ASSIGMENT(assignment)
                parent["ASSIGNMENT"] = assignment
                if self.tokens[self.currentToken].get_word() == ";": self.currentToken += 1
                else: self.exitParser(3, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())
            elif self.tokens[self.currentToken].get_word() == "int":
                variable = {}
                self.RULE_VARIABLE(variable)
                parent["VARIABLE"] = variable
                if self.tokens[self.currentToken].get_word() == ";": self.currentToken += 1
                else: self.exitParser(3, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())
            elif self.tokens[self.currentToken].get_word() == "while":
                while_block = {}
                self.RULE_WHILE(while_block)
                parent["WHILE"] = while_block
            elif self.tokens[self.currentToken].get_word() == "if":
                if_block = {}
                self.RULE_IF(if_block)
                parent["IF"] = if_block
            elif self.tokens[self.currentToken].get_word() == "print":
                print_block = {}
                self.RULE_PRINT(print_block)
                parent["PRINT"] = print_block
                if self.tokens[self.currentToken].get_word() == ";": self.currentToken += 1
                else: self.exitParser(3, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())
            elif self.tokens[self.currentToken].get_word() == "return":
                return_block = {}
                self.RULE_RETURN(return_block)
                parent["RETURN"] = return_block
                if self.tokens[self.currentToken].get_word() == ";": self.currentToken += 1
                else: self.exitParser(3, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())
            else: self.exitParser(4, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

    def RULE_ASSIGMENT(self, parent):
        parent["ID"] = self.tokens[self.currentToken].get_word()
        self.currentToken += 1

        if self.tokens[self.currentToken].get_word() == "=": self.currentToken += 1
        else: self.exitParser(5, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

        parent["EXPRESSION"] = self.tokens[self.currentToken].get_word()
        self.currentToken += 1

    def RULE_VARIABLE(self, parent):
        parent["TYPE"] = self.tokens[self.currentToken].get_word()
        self.currentToken += 1

        if self.tokens[self.currentToken].get_token() == "ID":
            parent["ID"] = self.tokens[self.currentToken].get_word()
            self.currentToken += 1
        else: self.exitParser(6, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

        if self.tokens[self.currentToken].get_word() == "=":
            self.currentToken += 1
            parent["EXPRESSION"] = self.tokens[self.currentToken].get_word()
            self.currentToken += 1

    def RULE_WHILE(self, parent):
        parent["WHILE"] = self.tokens[self.currentToken].get_word()
        self.currentToken += 1

        if self.tokens[self.currentToken].get_word() == "(": self.currentToken += 1
        else: self.exitParser(7, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

        parent["CONDITION"] = self.tokens[self.currentToken].get_word()
        self.currentToken += 1

        if self.tokens[self.currentToken].get_word() == ")": self.currentToken += 1
        else: self.exitParser(8, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

        if self.tokens[self.currentToken].get_word() == "{": self.currentToken += 1
        else: self.exitParser(1, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

        self.RULE_BODY(parent)

        if self.tokens[self.currentToken].get_word() == "}": self.currentToken += 1
        else: self.exitParser(2, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

    def RULE_IF(self, parent):
        parent["IF"] = self.tokens[self.currentToken].get_word()
        self.currentToken += 1

        if self.tokens[self.currentToken].get_word() == "(": self.currentToken += 1
        else: self.exitParser(7, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

        parent["CONDITION"] = self.tokens[self.currentToken].get_word()
        self.currentToken += 1

        if self.tokens[self.currentToken].get_word() == ")": self.currentToken += 1
        else: self.exitParser(8, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

        if self.tokens[self.currentToken].get_word() == "{": self.currentToken += 1
        else: self.exitParser(1, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

        self.RULE_BODY(parent)

        if self.tokens[self.currentToken].get_word() == "}": self.currentToken += 1
        else: self.exitParser(2, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

    def RULE_PRINT(self, parent):
        parent["PRINT"] = self.tokens[self.currentToken].get_word()
        self.currentToken += 1

        parent["EXPRESSION"] = self.tokens[self.currentToken].get_word()
        self.currentToken += 1

    def RULE_RETURN(self, parent):
        parent["RETURN"] = self.tokens[self.currentToken].get_word()
        self.currentToken += 1

        parent["EXPRESSION"] = self.tokens[self.currentToken].get_word()
        self.currentToken += 1
