class CodeGenerator:
    __variables = []
    __labels = []
    __instructions = []

    @staticmethod
    def addInstruction(instruction, p1, p2):
        CodeGenerator.__instructions.append(f"{instruction} {p1}, {p2}")
    
    @staticmethod
    def addLabel(name, value):
        CodeGenerator.__labels.append(f"#{name}, int, {value}")

    @staticmethod
    def addVariable(type, name):
        CodeGenerator.__variables.append(f"{name}, {type}, global, null")

    @staticmethod
    def writeCode():
        for variable in CodeGenerator.__variables:
            print(variable)
        for label in CodeGenerator.__labels:
            print(label)
        print("@")
        for inst in CodeGenerator.__instructions:
            print(inst)
    
    @staticmethod
    def clear():
        CodeGenerator.__instructions = []
        CodeGenerator.__labels = []
        CodeGenerator.__variables = []

    @staticmethod
    def getInstructionCount():
        return len(CodeGenerator.__instructions)
