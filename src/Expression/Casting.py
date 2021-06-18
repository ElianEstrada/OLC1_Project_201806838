from src.Abstract.Instruction import Instruction
from src.SymbolTable.Errors import Error
from src.SymbolTable.Type import type


class Casting(Instruction):

    def __init__(self, type, exp, row, column):
        self.__type = type
        self.__exp = exp
        self.row = row
        self.column = column

    
    def interpret(self, tree, table):

        if self.__type not in (type.BOOLEAN, type.STRING):
            if self.__exp != None:

                value = self.__exp.interpret(tree, table)

                if isinstance(value, Error):
                    return value

            if self.__type == type.INTEGGER:

                if self.__exp.get_type() == type.FLOAT:
                    return int(value)

                elif self.__exp.get_type() == type.INTEGGER:
                    return value
                
                elif self.__exp.get_type() == type.CHAR:
                    return ord(value)    
                
        else: 
            return Error("Semantic", f"Can't cast the type: {self.__type.name}")
            

    def get_type(self):
        return self.__type