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

        if self.__type not in (type.ARRAY, type.NULL):
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
                    
                    elif self.__exp.get_type() == type.STRING:
                        try: 
                            return int(value)
                        except ValueError:
                            return Error("Semantic", f"This value: {value} cannot be cast to INTEGGER", self.row, self.column)

                    else:
                        return Error("Semantic", f"{self.__exp.get_type().name} type cannot cast to {self.__type.name} type", self.row, self.column)

                elif self.__type == type.FLOAT:

                    if self.__exp.get_type() == type.FLOAT:
                        return value
                    
                    elif self.__exp.get_type() == type.INTEGGER:
                        return float(value)

                    elif self.__exp.get_type() == type.CHAR:
                        return float(ord(value))

                    elif self.__exp.get_type() == type.STRING:
                        try: 
                            return float(value)
                        except ValueError:
                            return Error("Semantic", f"This value: {value} cannot be cast to FLOAT", self.row, self.column)

                    else:
                        return Error("Semantic", f"{self.__exp.get_type().name} type cannot cast to {self.__type.name} type", self.row, self.column)
                    
                elif self.__type == type.STRING:

                    if self.__exp.get_type() == type.STRING:
                        return value
                    
                    elif self.__exp.get_type() == type.INTEGGER:
                        return str(value)

                    elif self.__exp.get_type() == type.FLOAT:
                        return str(value)

                    else:
                        return Error("Semantic", f"{self.__exp.get_type().name} type cannot cast to {self.__type.name} type", self.row, self.column)

                elif self.__type == type.CHAR:

                    if self.__exp.get_type() == type.CHAR:
                        return value

                    elif self.__exp.get_type() == type.INTEGGER:
                        if value >= 0 and value <=255:
                            return chr(value)
                        return Error("Semantic", f"The value: {value} out of range of type CHAR, this has range of 0-255", self.row, self.column)

                    else:
                        return Error("Semantic", f"{self.__exp.get_type().name} type cannot cast to {self.__type.name} type", self.row, self.column)
                
                elif self.__type == type.BOOLEAN:

                    if self.__exp.get_type() == type.STRING:
                        if value.lower() in ("true", "false"):
                            return value.lower()
                        else:
                            return Error("Semantic", f"This value: {value} cannot be cast to BOOLEAN", self.row, self.column)
                    else:
                        return Error("Semantic", f"{self.__exp.get_type().name} type cannot cast to {self.__type.name} type", self.row, self.column)
        else: 
            return Error("Semantic", f"Can't cast the type: {self.__type.name}")
            

    def get_type(self):
        return self.__type