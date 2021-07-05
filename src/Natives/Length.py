from src.SymbolTable.Errors import Error
from src.Instructions.Function import Function
from src.SymbolTable.Type import type

class Length(Function):

    def __init__(self, name, params, instructions, row, column):
        self.name = name
        self.params = params
        self.instructions = instructions
        self.type = type.NULL
        self.row = row
        self.column = column


    def interpret(self, tree, table):

        symbol = table.get_table('length##param1')

        if symbol == None:
            return Error("Semantic", "Identifier not found in the current context")

        if symbol.get_type() not in (type.STRING, type.ARRAY):
            return Error("Semantic", f"The type: {symbol.get_type().name} not valid like param for Length function", self.row, self.column)

        self.type = type.INTEGGER

        if symbol.get_type() == type.STRING:

            return len(symbol.get_value())
        else: 
            return self.calc_positions(symbol.get_value().get_list_value())

    
    def calc_positions(self, list_values):

        if isinstance(list_values, list):
            return len(list_values) * self.calc_positions(list_values[0])

        return 1


    def get_type(self):
        return self.type