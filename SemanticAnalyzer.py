from SymbolTableItem import SymbolTableItem
from collections import deque

class SemanticAnalyzer:
    __symbolTable = dict()
    __stack = deque()

    # create here a data structure for the cube of types
    __INT = 0
    __FLOAT = 1
    __CHAR = 2
    __STRING = 3
    __BOOLEAN = 4
    __VOID = 5
    __ERROR = 6
    __OP_MIN_MUL_DIV = 0
    __OP_PLU = 1
    __OP_NEG = 2
    __OP_GRE_LES = 3
    __OP_EQEQ_NOEQ = 4
    __OP_AND_OR = 5
    __OP_NOT = 6

    # Cube
    __cube = [[["int", "float", "error", "error", "error", "error", "error"],
                ["float", "float", "error", "error", "error", "error", "error"],
                ["error", "error", "error", "error", "error", "error", "error"],
                ["error", "error", "error", "error", "error", "error", "error"],
                ["error", "error", "error", "error", "error", "error", "error"],
                ["error", "error", "error", "error", "error", "error", "error"],
                ["error", "error", "error", "error", "error", "error", "error"]],
			   [["int", "float", "error", "string", "error", "error", "error"],
                ["float", "float", "error", "string", "error", "error", "error"],
                ["error", "error", "error", "string", "error", "error", "error"],
                ["string", "string", "string", "string", "string", "error", "error"],
                ["error", "error", "error", "string", "error", "error", "error"],
                ["error", "error", "error", "error", "error", "error", "error"],
                ["error", "error", "error", "error", "error", "error", "error"]],
               [["int", "float", "error", "error", "error", "error", "error"]],
		       [["boolean", "boolean", "error", "error", "error", "error", "error"],
                ["boolean", "boolean", "error", "error", "error", "error", "error"],
                ["error", "error", "error", "error", "error", "error", "error"],
                ["error", "error", "error", "error", "error", "error", "error"],
                ["error", "error", "error", "error", "error", "error", "error"],
                ["error", "error", "error", "error", "error", "error", "error"],
                ["error", "error", "error", "error", "error", "error", "error"]],
			   [["boolean", "boolean", "error", "error", "error", "error", "error"],
                ["boolean", "boolean", "error", "error", "error", "error", "error"],
                ["error", "error", "boolean", "error", "error", "error", "error"],
                ["error", "error", "error", "boolean", "error", "error", "error"],
                ["error", "error", "error", "error", "boolean", "error", "error"],
                ["error", "error", "error", "error", "error", "error", "error"],
                ["error", "error", "error", "error", "error", "error", "error"]],
               [["error", "error", "error", "error", "error", "error", "error"],
                ["error", "error", "error", "error", "error", "error", "error"],
                ["error", "error", "error", "error", "error", "error", "error"],
                ["error", "error", "error", "error", "error", "error", "error"],
                ["error", "error", "error", "error", "boolean", "error", "error"],
                ["error", "error", "error", "error", "error", "error", "error"],
                ["error", "error", "error", "error", "error", "error", "error"]],
               [["error", "error", "error", "error", "boolean", "error", "error"]]]
    
    @staticmethod
    def getSymbolTable():
        return SemanticAnalyzer.__symbolTable

    @staticmethod
    def CheckVariable(type, id, lineNo):
        if not (id in SemanticAnalyzer.__symbolTable):
            v = []
            if type == "string": v.append(SymbolTableItem(type, "global", ""))
            elif type == "void": v.append(SymbolTableItem(type, "global", ""))
            elif type == "int": v.append(SymbolTableItem(type, "global", "0"))
            elif type == "float": v.append(SymbolTableItem(type, "global", "0.0"))
            elif type == "char": v.append(SymbolTableItem(type, "global", "''"))
            elif type == "boolean": v.append(SymbolTableItem(type, "global", "false"))
            SemanticAnalyzer.__symbolTable[id] = v
        else:
            SemanticAnalyzer.error(1, lineNo, id)
            # error(1): "variable id is already defined"

    @staticmethod
    def pushStack(type):
		# push type in the stack
        SemanticAnalyzer.__stack.append(type);

    @staticmethod
    def popStack():
        result = ""
		# pop a value from the stack
        if SemanticAnalyzer.__stack:
            result = str(SemanticAnalyzer.__stack.pop())
        return result
    
    @staticmethod
    def calculate_cube(type, operator):
        result = ""
        Dim1 = 2
        Dim3 = 6
        Dim2 = 0  # Debido al operador unario

        type_dict = {
            "int": SemanticAnalyzer.__INT,
            "float": SemanticAnalyzer.__FLOAT,
            "char": SemanticAnalyzer.__CHAR,
            "string": SemanticAnalyzer.__STRING,
            "boolean": SemanticAnalyzer.__BOOLEAN,
            "void": SemanticAnalyzer.__VOID,
            "error": SemanticAnalyzer.__ERROR
        }

        if type in type_dict:
            Dim3 = type_dict[type]

        if operator == "-":
            Dim1 = SemanticAnalyzer.__OP_NEG
        elif operator == "!":
            Dim1 = SemanticAnalyzer.__OP_NOT

        result = SemanticAnalyzer.__cube[Dim1][Dim2][Dim3]
        return result
    
    @staticmethod
    def calculate_cube(type1, type2, operator):
        result = ""
        Dim1 = 2
        Dim2 = 6
        Dim3 = 6 

        type_dict = {
            "int": SemanticAnalyzer.__INT,
            "float": SemanticAnalyzer.__FLOAT,
            "char": SemanticAnalyzer.__CHAR,
            "string": SemanticAnalyzer.__STRING,
            "boolean": SemanticAnalyzer.__BOOLEAN,
            "void": SemanticAnalyzer.__VOID,
            "error": SemanticAnalyzer.__ERROR
        }

        if type1 in type_dict:
            Dim2 = type_dict[type1]

        if type2 in type_dict:
            Dim3 = type_dict[type2]

        if operator == "-" or operator == "*" or operator == "/":
            Dim1 = SemanticAnalyzer.__OP_MIN_MUL_DIV
        elif operator == "+":
            Dim1 = SemanticAnalyzer.__OP_PLU
        elif operator == "<" or operator == ">":
            Dim1 = SemanticAnalyzer.__OP_GRE_LES
        elif operator == "==" or operator == "!=":
            Dim1 = SemanticAnalyzer.__OP_EQEQ_NOEQ
        elif operator == "&" or operator == "|":
            Dim1 = SemanticAnalyzer.__OP_AND_OR
        elif operator == "=":
            if (type1 == type2) or (type2 == "float") and (type1 == "int"):
                result = "OK"
            return result
        result = SemanticAnalyzer.__cube[Dim1][Dim2][Dim3]
        return result
    
    @staticmethod
    def error(err, n, info):
        if err == 0:
            print(f"Line {n}:[Semantic] variable <{info}> not found")
        elif err == 1:
            print(f"Line {n}:[Semantic] variable <{info}> is already defined")
        elif err == 2:
            print(f"Line {n}:[Semantic] incompatible types: type mismatch")
        elif err == 3:
            print(f"Line {n}:[Semantic] incompatible types: expected boolean")
        elif err == 4:
            print(f"Line {n}:[Semantic] incompatible types: expected integer / octal / hexadecimal / binary")

    @staticmethod
    def getIdType(Id, line_no):
        temp = SemanticAnalyzer.__symbolTable.get(Id)
        if temp is None:
            SemanticAnalyzer.error(0, line_no, Id)
            return "error"
        return temp[0].getType()
    
    @staticmethod
    def clear_all():
        SemanticAnalyzer.getSymbolTable().clear()
        while SemanticAnalyzer.__stack:
            SemanticAnalyzer.__stack.pop()
