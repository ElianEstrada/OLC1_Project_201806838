from src.SymbolTable.Errors import Error
from src.Instructions.Function import Function
from src.SymbolTable.Type import type
import math

class Round(Function):

    def __init__(self, name, params, instructions, row, column):
        self.name = name
        self.params = params
        self.instructions = instructions
        self.type = type.NULL
        self.row = row
        self.column = column


    def interpret(self, tree, table):

        symbol = table.get_table('round##param1')

        if symbol == None:
            return Error("Semantic", "Identifier not found in the current context")

        if symbol.get_type() not in (type.INTEGGER, type.FLOAT):
            return Error("Semantic", f"The type: {symbol.get_type().name} not valid like param for Round function", self.row, self.column)
    
        self.type = type.INTEGGER

        if str(symbol.get_value()).split('.')[1][0] >= '5':
            return math.ceil(symbol.get_value())
        
        return round(symbol.get_value())

    def get_type(self):
        return self.type