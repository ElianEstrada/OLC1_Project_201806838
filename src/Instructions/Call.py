from src.SymbolTable.SymbolTable import SymbolTable
from src.Abstract.Instruction import Instruction
from src.SymbolTable.Errors import Error


class Call(Instruction):

    def __init__(self, name, params, row, column):
        self.__name = name.lower()
        self.__params = params
        self.__type = None
        self.row = row
        self.column = column

    def interpret(self, tree, table):
        ob_function = tree.get_function(self.__name)

        if ob_function == None:
            return Error("Semantic", f"The function whit the name: {self.__name} doesn't exits", self.row, self.column)

        new_table = SymbolTable(tree.get_global_table())
        
        value = ob_function.interpret(tree, new_table)

        if isinstance(value, Error):
            return value

        self.__type = ob_function.get_type()

        return value

    def get_type(self):
        return self.__type