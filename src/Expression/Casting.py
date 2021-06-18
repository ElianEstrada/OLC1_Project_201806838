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

        if self.__type not in (type.BOOLEAN, type.ARRAY, type.NULL):
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
                        return Error("Semantic", f"{self.__exp.get_type().name} type cannot cast to {self.__type.name} type")

                elif self.__type == type.FLOAT:

                    if self.__exp.get_type() == type.FLOAT:
                        return value
                    
                    elif self.__exp.get_type() == type.INTEGGER:
                        return float(value)

                    elif self.__exp.get_type() == type.CHAR:
                        return float(ord(value))

                    else:
                        return Error("Semantic", f"{self.__exp.get_type().name} type cannot cast to {self.__type.name} type")
                    
                elif self.__type == type.STRING:

                    if self.__exp.get_type() == type.STRING:
                        return value
                    
                    elif self.__exp.get_type() == type.INTEGGER:
                        return str(value)

                    elif self.__exp.get_type() == type.FLOAT:
                        return str(value)

                    else:
                        return Error("Semantic", f"{self.__exp.get_type().name} type cannot cast to {self.__type.name} type")

                elif self.__type == type.CHAR:

                    if self.__exp.get_type() == type.CHAR:
                        return value

                    elif self.__exp.get_type() == type.INTEGGER:
                        return chr(value)

                    else:
                        return Error("Semantic", f"{self.__exp.get_type().name} type cannot cast to {self.__type.name} type")
                
        else: 
            return Error("Semantic", f"Can't cast the type: {self.__type.name}")
            

    def get_type(self):
        return self.__type