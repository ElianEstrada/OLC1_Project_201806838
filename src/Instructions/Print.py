from src.Abstract.Instruction import Instruction
from src.SymbolTable.Errors import Error
from src.SymbolTable.Type import type


class Print(Instruction):

    def __init__(self, expression, row, column): 
        self.__expression = expression
        self.row = row
        self.column = column

    def interpret(self, tree, table):
        value = self.__expression.interpret(tree, table)

        if isinstance(value, Error):
            return value

        if self.__expression.get_type() == type.ARRAY:
            return Error("Semantic", "Don't print the arrya complet", self.row, self.column)
        elif self.__expression.get_type() == type.NULL:
            return Error("Semantic", "NullPointer Exception", self.row, self.column)

        tree.update_console("> " + str(value))