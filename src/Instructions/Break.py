from src.Abstract.Instruction import Instruction
from src.SymbolTable.Errors import Error


class Break(Instruction):

    def __init__(self, row, column):
        self.row = row
        self.column = column

    def interpret(self, tree, table):
        return self