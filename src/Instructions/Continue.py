from src.Abstract.Ast_Node import Ast_Node
from src.Abstract.Instruction import Instruction


class Continue(Instruction): 

    def __init__(self, row, column):
        self.row = row
        self.column = column


    def interpret(self, tree, table):
        return self

    def get_node(self):
        node = Ast_Node("Continue")
        return node