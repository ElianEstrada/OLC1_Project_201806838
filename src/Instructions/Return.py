from src.Abstract.Ast_Node import Ast_Node
from src.Abstract.Instruction import Instruction
from src.SymbolTable.Errors import Error


class Return(Instruction):

    def __init__(self, expression, row, column):
        self.__expression = expression
        self.__type = None
        self.__result = None
        self.row = row
        self.column = column

    
    def interpret(self, tree, table):

        value = self.__expression.interpret(tree, table)

        if isinstance(value, Error):
            return value

        self.__type = self.__expression.get_type()
        self.__result = value

    
        return self

    def get_node(self):
        node = Ast_Node("Return")
        node.add_childs_node(self.__expression.get_node())

        return node

    def get_type(self):
        return self.__type

    def get_result(self):
        return self.__result
