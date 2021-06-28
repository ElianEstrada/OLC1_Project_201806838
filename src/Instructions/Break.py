from src.Abstract.Instruction import Instruction


class Break(Instruction):

    def __init__(self, row, column):
        self.row = row
        self.column = column

    def interpret(self, tree, table):
        return self