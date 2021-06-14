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


    def get_instructions(self):
        return self.__instructions

    def get_value(self):
        return self.__exp