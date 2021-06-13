from src.Abstract.Instruction import Instruction
from src.SymbolTable.Errors import Error
from src.SymbolTable.Type import type
from src.SymbolTable.Symbol import Symbol

class Declaration(Instruction):

    def __init__(self, id, row, column, expression = None):
        self.__id = id
        self.__expression = expression
        self.row = row
        self.column = column

    def interpret(self, tree, table):

        symbol = ""
        
        if self.__expression != None:
            value = self.__expression.interpret(tree, table)

            if isinstance(value, Error):
                return value
            
            symbol = Symbol(self.__id, self.__expression.get_type(), self.row, self.column, value)
        else:
            symbol = Symbol(self.__id, type.NULL, self.row, self.column, None)

        result = table.set_table(symbol)

        if isinstance(result, Error):
            return result

        return None

    def set_id(self, id):
        self.__id = id

    def get_id(self):
        return self.__id

    def set_value(self, value):
        self.__expression = value

    def get_value(self):
        return self.__expression