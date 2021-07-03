from src.Abstract.Instruction import Instruction
from src.Abstract.Ast_Node import Ast_Node
from src.SymbolTable.Errors import Error
from src.SymbolTable.Type import type


class Casting(Instruction):

    def __init__(self, type, exp, row, column):
        self.__type = type
        self.__exp = exp
        self.__value = None
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
                        self.__value = int(value)
                        return int(value)

                    elif self.__exp.get_type() == type.INTEGGER:
                        self.__value = value
                        return value
                    
                    elif self.__exp.get_type() == type.CHAR:
                        self.__value = ord(value)
                        return ord(value)
                    
                    elif self.__exp.get_type() == type.STRING:
                        try: 
                            self.__value = int(value)
                            return int(value)
                        except ValueError:
                            return Error("Semantic", f"This value: {value} cannot be cast to INTEGGER", self.row, self.column)

                    else:
                        return Error("Semantic", f"{self.__exp.get_type().name} type cannot cast to {self.__type.name} type", self.row, self.column)

                elif self.__type == type.FLOAT:

                    if self.__exp.get_type() == type.FLOAT:
                        self.__value = value
                        return value
                    
                    elif self.__exp.get_type() == type.INTEGGER:
                        self.__value = float(value)
                        return float(value)

                    elif self.__exp.get_type() == type.CHAR:
                        self.__value = float(ord(value))
                        return float(ord(value))

                    elif self.__exp.get_type() == type.STRING:
                        try: 
                            self.__value = float(value)
                            return float(value)
                        except ValueError:
                            return Error("Semantic", f"This value: {value} cannot be cast to FLOAT", self.row, self.column)

                    else:
                        return Error("Semantic", f"{self.__exp.get_type().name} type cannot cast to {self.__type.name} type", self.row, self.column)
                    
                elif self.__type == type.STRING:

                    if self.__exp.get_type() == type.STRING:
                        self.__value = value
                        return value
                    
                    elif self.__exp.get_type() == type.INTEGGER:
                        self.__value = str(value)
                        return str(value)

                    elif self.__exp.get_type() == type.FLOAT:
                        self.__value = str(value)
                        return str(value)

                    else:
                        return Error("Semantic", f"{self.__exp.get_type().name} type cannot cast to {self.__type.name} type", self.row, self.column)

                elif self.__type == type.CHAR:

                    if self.__exp.get_type() == type.CHAR:
                        self.__value = value
                        return value

                    elif self.__exp.get_type() == type.INTEGGER:
                        if value >= 0 and value <=255:
                            self.__value = chr(value)
                            return chr(value)
                        return Error("Semantic", f"The value: {value} out of range of type CHAR, this has range of 0-255", self.row, self.column)

                    else:
                        return Error("Semantic", f"{self.__exp.get_type().name} type cannot cast to {self.__type.name} type", self.row, self.column)
                
                elif self.__type == type.BOOLEAN:

                    if self.__exp.get_type() == type.STRING:
                        if value.lower() in ("true", "false"):
                            self.__value = value.lower()
                            return value.lower()
                        else:
                            return Error("Semantic", f"This value: {value} cannot be cast to BOOLEAN", self.row, self.column)
                    else:
                        return Error("Semantic", f"{self.__exp.get_type().name} type cannot cast to {self.__type.name} type", self.row, self.column)
        else: 
            return Error("Semantic", f"Can't cast the type: {self.__type.name}")
            

    def get_node(self):
        node = Ast_Node("Casting")
        node.add_child("(")
        node.add_child(self.__type.name)
        node.add_child(")")
        node.add_childs_node(self.__exp.get_node())

        return node

    def get_type(self):
        return self.__type

    def __str__(self):
        return str(self.__value)