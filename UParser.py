from Token import Token
from SemanticAnalyzer import SemanticAnalyzer
from CodeGenerator import CodeGenerator

class UParser:
    def __init__(self, tokens):
        self.currentToken = 0
        self.tokens = tokens
        self.FIRST = dict()
        self.FOLLOW = dict()
        self.buildFandF()
        self.newLineErr = False
        self.labelCount = 0
        self.progEnd = 0

    # Incompleta
    def buildFandF(self):
        self.FIRST["PROGRAM"] = {"{"}
        self.FIRST["PRINT"] = {"print"}
        self.FIRST["ASSIGMENT"] = {"ID"}
        self.FIRST["VARIABLE"] = {"int", "float", "bool", "void", "char", "string"}
        self.FIRST["RETURN"] = {"return"}
        self.FIRST["WHILE"] = {"while"}
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
        self.FOLLOW["RETURN"] = {";"}
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
        elif error == 11: 
            print("Line  "+str(line)+": invalid \""+str(word)+"\" expected IDENTIFIER")
            isIncremented = True

        if isIncremented: self.incrementToken()

    def run(self):
        SemanticAnalyzer.clear_all()
        CodeGenerator.clear()
        self.RULE_PROGRAM()
        CodeGenerator.writeCode();

    def RULE_PRINCIPAL(self):
        self.progEnd += 1
        if self.tokens[self.currentToken].get_word() == "int" or self.tokens[self.currentToken].get_word() == "float" or self.tokens[self.currentToken].get_word() == "bool" or self.tokens[self.currentToken].get_word() == "char" or self.tokens[self.currentToken].get_word() == "string" or self.tokens[self.currentToken].get_word() == "void":
            self.RULE_VARIABLE()
            if self.tokens[self.currentToken].get_word() == ";": self.incrementToken()
            else: self.exitParser(3, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())

    def RULE_PROGRAM(self):
        self.progEnd += 1
        if self.tokens[self.currentToken].get_word() == "{": self.incrementToken()
        else: 
            self.exitParser(1, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

            while not (self.isFirst(self.tokens[self.currentToken], "BODY") or self.tokens[self.currentToken].get_word() == "}"):
                self.incrementToken()

        self.RULE_BODY()

        if self.tokens[self.currentToken].get_word() == "}": 
            self.progEnd -= 1
            if self.progEnd == 0:
                CodeGenerator.addInstruction("OPR", "0", "0")
            self.incrementToken()
        else: self.exitParser(2, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

    def RULE_BODY(self):
        self.newLineErr = False
        currentLine = -1

        while self.tokens[self.currentToken].get_word() != "}":
            currentLine = self.tokens[self.currentToken].get_line()
            if self.tokens[self.currentToken].get_token() == "ID":
                self.RULE_ASSIGMENT()
                if self.tokens[self.currentToken].get_word() == ";" and self.isSameLine(): self.incrementToken()
                else: self.exitParser(3, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())
            elif self.tokens[self.currentToken].get_word() == "int" or self.tokens[self.currentToken].get_word() == "float" or self.tokens[self.currentToken].get_word() == "bool" or self.tokens[self.currentToken].get_word() == "char" or self.tokens[self.currentToken].get_word() == "string" or self.tokens[self.currentToken].get_word() == "void":
                self.RULE_VARIABLE()
                if self.tokens[self.currentToken].get_word() == ";" and self.isSameLine(): self.incrementToken()
                else: self.exitParser(3, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())
            elif self.tokens[self.currentToken].get_word() == "while":
                self.RULE_WHILE()
            # No estuvo en las reglas
            elif self.tokens[self.currentToken].get_word() == "do":
                self.RULE_DOWHILE()
                if self.tokens[self.currentToken].get_word() == ";": self.incrementToken()
                else: self.exitParser(3, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())
            # No estuvo en las reglas
            elif self.tokens[self.currentToken].get_word() == "for":
                self.RULE_FOR()
            elif self.tokens[self.currentToken].get_word() == "switch":
                self.RULE_SWITCH()
            elif self.tokens[self.currentToken].get_word() == "if":
                self.RULE_IF()
            elif self.tokens[self.currentToken].get_word() == "print":
                self.RULE_PRINT()
                if self.tokens[self.currentToken].get_word() == ";" and self.isSameLine(): self.incrementToken()
                else: self.exitParser(3, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())
            # No estuvo en las reglas
            elif self.tokens[self.currentToken].get_word() == "read":
                self.RULE_READ()
                if self.tokens[self.currentToken].get_word() == ";": self.incrementToken()
                else: self.exitParser(3, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())
            elif self.tokens[self.currentToken].get_word() == "return":
                self.RULE_RETURN()
                if self.tokens[self.currentToken].get_word() == ";" and self.isSameLine(): self.incrementToken()
                else: self.exitParser(3, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())
            else: 
                self.newLineErr = True
                self.exitParser(4, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())
                while currentLine == self.tokens[self.currentToken].get_line() and (not (self.isFirst(self.tokens[self.currentToken], "BODY") or self.isFirst(self.tokens[self.currentToken], "BODY"))):
                    self.incrementToken()
            '''
            if self.currentToken == len(self.tokens) - 1:
                break
            '''

    def RULE_ASSIGMENT(self):
        id = ""

        if self.tokens[self.currentToken].get_token() == "ID":
            # Semantic
            SemanticAnalyzer.pushStack(SemanticAnalyzer.getIdType(self.tokens[self.currentToken].get_word(), self.tokens[self.currentToken].get_line()))
            
            # Code Generation
            id = self.tokens[self.currentToken].get_word()

            self.incrementToken()  

            if self.tokens[self.currentToken].get_word() == "="and self.isSameLine(): self.incrementToken()
            else: 
                self.exitParser(5, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())
                while self.isSameLine() and (not (self.isFirst(self.tokens[self.currentToken], "EXPRESSION") or self.isFirst(self.tokens[self.currentToken], "EXPRESSION"))):
                    self.incrementToken()  

            self.RULE_EXPRESSION()

            # Semantic
            x = SemanticAnalyzer.popStack()
            y = SemanticAnalyzer.popStack()
            result = SemanticAnalyzer.calculate_cube(x, y, "=")
            if (not result == "OK") and (not y == ""):
                SemanticAnalyzer.error(2, self.tokens[self.currentToken-1].get_line(), "")
            
            # Code Generation
            CodeGenerator.addInstruction("STO", id, "0");
     
    # Incompleta
    def RULE_FUNCTION(self):
        self.incrementToken()
    
        if self.tokens[self.currentToken].get_token() == "ID": self.incrementToken()
        else: self.exitParser(6, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())

        if self.tokens[self.currentToken].get_word() == "(": self.incrementToken()
        else: self.exitParser(7, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())

        while not (self.tokens[self.currentToken].get_word() in self.FIRST["PARAMS"] or self.tokens[self.currentToken].get_token() in self.FIRST["PARAMS"] or self.tokens[self.currentToken].get_word() == ")"):
            self.incrementToken() 

        self.RULE_EXPRESSION()

        if self.tokens[self.currentToken].get_word() == ")": self.incrementToken()
        else: self.exitParser(8, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())

    def RULE_VARIABLE(self):
        type = ""
        id = ""

        # Code Generation
        type = self.tokens[self.currentToken].get_word()

        self.incrementToken()
    
        if self.tokens[self.currentToken].get_token() == "ID" and self.isSameLine(): 
            # Semantic
            SemanticAnalyzer.CheckVariable(self.tokens[self.currentToken-1].get_word(), self.tokens[self.currentToken].get_word(), self.tokens[self.currentToken].get_line())
            
            # Code Generation
            id = self.tokens[self.currentToken].get_word()
        else:
            self.exitParser(6, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())

        # Code Generation
        CodeGenerator.addVariable(type, id)

        # Declaration and assigment
        if self.tokens[self.currentToken].get_word() == "=": 
            self.RULE_ASSIGMENT()
        else: self.incrementToken()
            
    def RULE_WHILE(self):
        e1 = "" + self.labelCount
        self.labelCount += 1
        e2 = "" + self.labelCount
        self.labelCount += 1

        self.incrementToken()

        if self.tokens[self.currentToken].get_word() == "(" and self.isSameLine(): 
            # Code Generation
            CodeGenerator.addLabel(e1, CodeGenerator.getInstructionCount() + 1)

            self.incrementToken()
        else: 
            self.exitParser(7, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())

            while self.isSameLine() and (not (self.isFirst(self.tokens[self.currentToken], "EXPRESSION") or self.isFirst(self.tokens[self.currentToken], "PROGRAM") or self.tokens[self.currentToken].get_word() == ")")):
                self.incrementToken()

        self.RULE_EXPRESSION()

        # Semantic
        x = SemanticAnalyzer.popStack()
        if not x == "boolean":
            SemanticAnalyzer.error(3, self.tokens[self.currentToken-1].get_line(), "")

        # Code Generation
        CodeGenerator.addInstruction("JMC", "#" + e2, "false")

        if self.tokens[self.currentToken].get_word() == ")" and self.isSameLine(): self.incrementToken()
        else: 
            self.exitParser(8, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())
            while self.isSameLine() and (not self.isFirst(self.tokens[self.currentToken], "PROGRAM")):
                self.incrementToken()

        self.RULE_PROGRAM()

        # Code Generation
        CodeGenerator.addInstruction("JMP", "#" + e1, "0")
        CodeGenerator.addLabel(e2, CodeGenerator.getInstructionCount() + 1)

    # Por incluir
    def RULE_DOWHILE(self):
        self.incrementToken()

        self.RULE_PROGRAM()

        if self.tokens[self.currentToken].get_word() == "(": self.incrementToken()
        else: self.exitParser(7, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())

        while not (self.tokens[self.currentToken].get_word() in self.FIRST["EXPRESSION"] or self.tokens[self.currentToken].get_token() in self.FIRST["EXPRESSION"] or self.tokens[self.currentToken].get_word() == ")"):
            self.incrementToken() 

        self.RULE_EXPRESSION()

        if self.tokens[self.currentToken].get_word() == ")": self.incrementToken()
        else: self.exitParser(8, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())
    
    # Incompleta
    def RULE_SWITCH(self):
        self.incrementToken()
        #Por implementar

    # Por incluir
    def RULE_FOR(self):
        self.incrementToken()

        if self.tokens[self.currentToken].get_word() == "(": self.incrementToken()
        else: self.exitParser(7, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())

        while not (self.tokens[self.currentToken].get_word() in self.FIRST["PARAMS"] or self.tokens[self.currentToken].get_token() in self.FIRST["PARAMS"] or self.tokens[self.currentToken].get_word() == ")"):
            self.incrementToken() 

        self.RULE_PARAMS_FOR()

        if self.tokens[self.currentToken].get_word() == ")": self.incrementToken()
        else: self.exitParser(8, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())
    
    # Por incluir
    def RULE_PARAMS_FOR(self):
        if self.tokens[self.currentToken].get_word() == "int" or self.tokens[self.currentToken].get_word() == "float" or self.tokens[self.currentToken].get_word() == "bool" or self.tokens[self.currentToken].get_word() == "char" or self.tokens[self.currentToken].get_word() == "string" or self.tokens[self.currentToken].get_word() == "void":
            self.RULE_VARIABLE()
            if self.tokens[self.currentToken].get_word() == ";": self.incrementToken()
            else: self.exitParser(3, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())
        else: self.exitParser(4, self.tokens[self.currentToken].get_line(), self.tokens[self.currentToken].get_word())

        while not (self.tokens[self.currentToken].get_word() in self.FIRST["EXPRESSION"] or self.tokens[self.currentToken].get_token() in self.FIRST["EXPRESSION"] or self.tokens[self.currentToken].get_word() == ")"):
            self.incrementToken() 

        self.RULE_EXPRESSION()

        if self.tokens[self.currentToken].get_word() == ";": self.incrementToken()
        else: self.exitParser(3, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())

        while not (self.tokens[self.currentToken].get_word() in self.FIRST["E"] or self.tokens[self.currentToken].get_token() in self.FIRST["E"] or self.tokens[self.currentToken].get_word() == ")"):
            self.incrementToken() 

        self.RULE_E()

    def RULE_IF(self):
        e1 = "" + self.labelCount
        self.labelCount += 1
        e2 = "" + self.labelCount
        self.labelCount += 1

        self.incrementToken()

        if self.tokens[self.currentToken].get_word() == "(" and self.isSameLine(): self.incrementToken()
        else: 
            self.exitParser(7, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())
            while self.isSameLine() and (not (self.isFirst(self.tokens[self.currentToken], "EXPRESSION") or self.isFirst(self.tokens[self.currentToken], "PROGRAM") or self.tokens[self.currentToken].get_word() == "else" or self.tokens[self.currentToken].get_word() == ")")):
                self.incrementToken()

        self.RULE_EXPRESSION()

        # Semantic
        x = SemanticAnalyzer.popStack()
        if not x == "boolean":
            SemanticAnalyzer.error(3, self.tokens[self.currentToken-1].get_line(), "")

        # Code Generation
        CodeGenerator.addInstruction("JMC", "#" + e1, "false")

        if self.tokens[self.currentToken].get_word() == ")" and self.isSameLine(): self.incrementToken()
        else: 
            self.exitParser(8, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())
            while self.isSameLine() and (not self.isFirst(self.tokens[self.currentToken], "PROGRAM") or self.tokens[self.currentToken].get_word() == "else"):
                self.incrementToken()

        self.RULE_PROGRAM()

        if self.tokens[self.currentToken].get_word() == "else": 
            # Code Generation
            CodeGenerator.addLabel(e1, CodeGenerator.getInstructionCount + 2)
            CodeGenerator.addInstruction("JMP", "#" + e2, "0")

            self.incrementToken()
            self.RULE_PROGRAM()

            # Code Generation
            CodeGenerator.addLabel(e2, CodeGenerator.getInstructionCount + 1)
        else: CodeGenerator.addLabel(e1, CodeGenerator.getInstructionCount + 1)

    def RULE_RETURN(self):
        # Code Generation
        CodeGenerator.addInstruction("OPR", "1", "0")

        self.incrementToken()

    def RULE_PRINT(self):
        self.incrementToken()

        if self.tokens[self.currentToken].get_word() == "(" and self.isSameLine(): self.incrementToken()
        else: 
            self.exitParser(7, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())
            while self.isSameLine() and (not (self.isFirst(self.tokens[self.currentToken], "EXPRESSION") or self.tokens[self.currentToken].get_word() == ")")):
                self.incrementToken()

        self.RULE_EXPRESSION()

        if self.tokens[self.currentToken].get_word() == ")" and self.isSameLine(): 
            self.incrementToken()

            # Code Generation
            CodeGenerator.addInstruction("OPR", "21", "0")
        else: self.exitParser(8, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())

    # Por incluir
    def RULE_READ(self):
        self.incrementToken()

        if self.tokens[self.currentToken].get_word() == "(": 
            self.incrementToken()

            if self.tokens[self.currentToken].get_token() == "ID": self.incrementToken()
            else: self.exitParser(11, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())

            if self.tokens[self.currentToken].get_word() == ")": self.incrementToken()
            else: self.exitParser(8, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())
        else: self.exitParser(7, self.tokens[self.currentToken-1].get_line(), self.tokens[self.currentToken].get_word())

        while not (self.tokens[self.currentToken].get_word() in self.FIRST["EXPRESSION"] or self.tokens[self.currentToken].get_token() in self.FIRST["EXPRESSION"] or self.tokens[self.currentToken].get_word() == ")"):
            self.incrementToken() 

    def RULE_EXPRESSION(self):
        self.RULE_X()

        while self.isSameLine() and self.tokens[self.currentToken].get_word() == "|": 
            self.incrementToken()
            self.RULE_X()

            # Semantic
            x = SemanticAnalyzer.popStack()
            y = SemanticAnalyzer.popStack()
            result = SemanticAnalyzer.calculate_cube(x, y, "|")
            SemanticAnalyzer.pushStack(result)

            # Code Generation
            CodeGenerator.addInstruction("OPR", "8", "0")

    def RULE_X(self):
        self.RULE_Y()

        while self.isSameLine() and self.tokens[self.currentToken].get_word() == "&": 
            self.incrementToken()
            self.RULE_Y()

            # Semantic
            x = SemanticAnalyzer.popStack()
            y = SemanticAnalyzer.popStack()
            result = SemanticAnalyzer.calculate_cube(x, y, "&")
            SemanticAnalyzer.pushStack(result)

            # Code Generation
            CodeGenerator.addInstruction("OPR", "9", "0")

    def RULE_Y(self):
        operatorWasUsed = False
        
        if self.tokens[self.currentToken].get_word() == "!" and self.isSameLine(): 
            # Semantic
            operatorWasUsed = True

            self.incrementToken()
            
        self.RULE_R()

        if operatorWasUsed:
            # Semantic
            x = SemanticAnalyzer.popStack()
            y = SemanticAnalyzer.popStack()
            result = SemanticAnalyzer.calculate_cube(x, y, "!")
            SemanticAnalyzer.pushStack(result)

            # Code Generation
            CodeGenerator.addInstruction("OPR", "10", "0")

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
        #Falat CodeGeneration
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

    def isFirst(self, token, scope):
        return (token.get_word() in self.FIRST[scope] or token.get_token() in self.FIRST[scope])
    
    def isFollow(self, token, scope):
        return (token.get_word() in self.FOLLOW[scope] or token.get_token() in self.FOLLOW[scope])

    def isSameLine(self):
        return (self.tokens[self.currentToken].get_line() == self.tokens[self.currentToken - 1].get_line())