class SymbolTableItem:
    def __init__(self, type, scope, value):
        self.setType(type)
        self.setScope(scope)
        self.setValue(value)
    
    def getType(self):
        return self.__type
    
    def setType(self, type):
        self.__type = type
    
    def getScope(self):
        return self.__scope
    
    def setScope(self, scope):
        self.__scope = scope

    def getValue(self):
        return self.__value
    
    def setValue(self, value):
        self.__value = value