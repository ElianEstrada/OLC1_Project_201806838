from src.Abstract.Instruction import Instruction


class Continue(Instruction): 

    def __init__(self, row, column):
        self.row = row
        self.column = column


    def interpret(self, tree, table):
        return self