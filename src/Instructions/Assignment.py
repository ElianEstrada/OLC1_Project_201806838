from src.Abstract.Instruction import Instruction
from src.SymbolTable.Symbol import Symbol
from src.SymbolTable.Errors import Error
from src.SymbolTable.Type import type

class Assignment(Instruction):

    def __init__(self, id, expression, row, column):
        self.__id = id
        self.__expression = expression
        self.row = row
        self.column = column

    
    def interpret(self, tree, table):
            
        value = self.__expression.interpret(tree, table)

        if isinstance(value, Error):
            return value

        new_symbol = Symbol(self.__id, self.__expression.get_type(), self.row, self.column, value)

        result = table.update_table(new_symbol)

        if isinstance(result, Error):
            return result
        
        return None
            


    def set_id(self, id):
        self.__id = id

    def get_id(self):
        return self.__id

    def set_expression(self, expression):
        self.__expression = expression
    
    def get_expression(self):
        return self.__expression