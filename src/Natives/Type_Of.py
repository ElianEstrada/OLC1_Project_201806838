from src.SymbolTable.Errors import Error
from src.Instructions.Function import Function
from src.SymbolTable.Type import type

class Type_Of(Function):

    def __init__(self, name, params, instructions, row, column):
        self.name = name
        self.params = params
        self.instructions = instructions
        self.type = type.STRING
        self.row = row
        self.column = column


    def interpret(self, tree, table):

        symbol = table.get_table('type_of##param1')

        if symbol == None:
            return Error("Semantic", "Identifier not found in the current context")
        
        if symbol.get_type() == type.ARRAY:
            return f"{symbol.get_type().name} -> {symbol.get_value().get_type().name}"

        return symbol.get_type().name

    def get_type(self):
        return self.type