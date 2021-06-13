from src.Abstract.Instruction import Instruction
from src.SymbolTable.Errors import Error


class Identifier(Instruction):

    def __init__(self, id, row, column):
        self.__id = id
        self.__type = None
        self.row = row
        self.column = column


    def interpret(self, tree, table):
        
        symbol = table.get_table(self.__id.lower())

        if symbol == None:
            return Error("Semantic", f"The id: {self.__id} doesn't exist in current context", self.row, self.column)

        self.__type = symbol.get_type()

        return symbol.get_value()

    
    def set_id(self, id):
        self.__id = id

    def get_id(self):
        return self.__id

    def set_type(self, type):
        self.__type = type

    def get_type(self):
        return self.__type