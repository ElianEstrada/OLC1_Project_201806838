from src.SymbolTable.Errors import Error
from src.Instructions.Function import Function
from src.SymbolTable.Type import type

class To_Lower(Function):

    def __init__(self, name, params, instructions, row, column):
        self.name = name
        self.params = params
        self.instructions = instructions
        self.type = type.NULL
        self.row = row
        self.column = column


    def interpret(self, tree, table):

        symbol = table.get_table('to_lower##param1')

        if symbol == None:
            return Error("Semantic", "Identifier not found in the current context", self.row, self.column)

        if symbol.get_type() != type.STRING:
            return Error("Semantic", f"The type: {symbol.get_type().name} not valid like param for toLower function", self.row, self.column)
        
        self.__type = type.STRING
        return symbol.get_value().lower()

    def get_type(self):
        return self.type
