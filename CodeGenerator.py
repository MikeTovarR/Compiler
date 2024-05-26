class CodeGenerator:
    __variables = []
    __labels = []
    __instructions = []

    @classmethod
    def addInstruction(instruction, p1, p2):
        CodeGenerator.__instructions.append(instruction + " " + p1 + ", " + p2)
    
    @classmethod
    def addLabel(name, value):
        CodeGenerator.__labels.append("#" + name + ", int, " + value)

    @classmethod
    def addVariable(type, name):
        CodeGenerator.__variables.append(name + ", " + type + ", global, null")

    @classmethod
    def writeCode(type, name):
        for variable in CodeGenerator.__variables:
            print(variable)
        for label in CodeGenerator.__labels:
            print(label)
        print("@")
        for inst in CodeGenerator.__instructions:
            print(inst)
    
    @classmethod
    def clear():
        CodeGenerator.__instructions = []
        CodeGenerator.__labels = []
        CodeGenerator.__variables = []

    @classmethod
    def getInstructionCount():
        return len(CodeGenerator.__instructions)
