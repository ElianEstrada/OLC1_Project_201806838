from src.Abstract.Ast_Node import Ast_Node
from src.Abstract.Instruction import Instruction
from src.SymbolTable.Errors import Error


class Case(Instruction):

    def __init__(self, exp, instructions, row, column):
        self.__exp = exp
        self.__instructions = instructions
        self.row = row
        self.column = column

    
    def interpret(self, tree, table):
        
        return self.__exp.interpret(tree, table)


    def get_node(self):
        node = Ast_Node("Case")
        node.add_child("case")
        node.add_childs_node(self.__exp.get_node())
        node.add_child(":")
        
        instructions = Ast_Node("Instructions")
        for inst in self.__instructions:
            instructions.add_childs_node(inst.get_node())

        node.add_childs_node(instructions)

        return node

    def get_instructions(self):
        return self.__instructions

    def get_value(self):
        return self.__exp