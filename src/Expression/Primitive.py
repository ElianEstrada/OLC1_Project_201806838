from src.Abstract.Instruction import Instruction
from src.Abstract.Ast_Node import Ast_Node

class Primitive(Instruction):

    def __init__(self, type, value, row, column):
        self.__type = type
        self.__value = value
        self.row = row
        self.column = column

    def interpret(self, tree, table):
        return self.__value

    def get_node(self):
        node = Ast_Node("Primitive")
        node.add_child(str(self.__value))
        return node

    def set_type(self, type):
        self.__type = type
    
    def get_type(self):
        return self.__type

    def set_value(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

    def __str__(self):
        return str(self.__value)

        