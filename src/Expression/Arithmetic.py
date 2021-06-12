from src.Abstract.Instruction import Instruction
from src.SymbolTable.Errors import Error
from src.SymbolTable.Type import type, Arithmetic_Operator

class Arithmetic(Instruction):

    def __init__(self, exp1, exp2, operator, row, column):
        self.__operator = operator
        self.__exp1 = exp1
        self.__exp2 = exp2
        self.row = row
        self.column = column
        self.__type = None
        self.__bolean = {
            "true": True,
            "false": False
        }

    def interpret(self, tree, table):
        left = self.__exp1.interpret(tree, table)

        if isinstance(left, Error):
            return left

        if self.__exp2 != None:

            right = self.__exp2.interpret(tree, table)

            if isinstance(right, Error):
                return right
        
            if self.__operator == Arithmetic_Operator.ADDITION:
                
                print(self.__exp1.get_type())
                if self.__exp1.get_type() == type.INTEGGER:

                    if self.__exp2.get_type() == type.INTEGGER:
                        self.__type = type.INTEGGER
                        return int(left) + int(right)
                    elif self.__exp2.get_type() == type.FLOAT:
                        self.__type = type.FLOAT
                        return float(left) + float(right)
                    elif self.__exp2.get_type() == type.STRING:
                        self.__type = type.STRING
                        return str(left) + right
                    elif self.__exp2.get_type() == type.BOOLEAN:
                        self.__type = type.INTEGGER
                        return int(left) + int(self.__bolean[right])
                    else:   
                        return Error("Semantic", f"The type: {self.__exp2.get_type().name} cannot be operated whit type: INTEGGER", self.row, self.column)

                elif self.__exp1.get_type() == type.FLOAT:
                    
                    if self.__exp2.get_type() in (type.INTEGGER, type.FLOAT):
                        self.__type = type.FLOAT
                        return float(left) + float(right)
                    elif self.__exp2.get_type() == type.STRING:
                        self.__type = type.STRING
                        return str(left) + right
                    elif self.__exp2.get_type() == type.BOOLEAN:
                        self.__type = type.FLOAT
                        return float(left) + float(self.__bolean[right])
                    else:   
                        return Error("Semantic", f"The type: {self.__exp2.get_type().name} cannot be operated whit type: FLOAT", self.row, self.column)
                
                elif self.__exp1.get_type() == type.BOOLEAN:

                    if self.__exp2.get_type() == type.INTEGGER:
                        self.__type = type.INTEGGER
                        return int(self.__bolean[left]) + int(right)
                    elif self.__exp2.get_type() == type.FLOAT:
                        self.__type = type.FLOAT
                        return float(self.__bolean[left]) + float(right)
                    elif self.__exp2.get_type() == type.STRING:
                        self.__type = type.STRING
                        return str(left) + right
                    elif self.__exp2.get_type() == type.BOOLEAN:
                        self.__type = type.INTEGGER
                        return float(self.__bolean[left]) + float(self.__bolean[right])
                    else:   
                        return Error("Semantic", f"The type: {self.__exp2.get_type().name} cannot be operated whit type: BOOLEAN", self.row, self.column)

                elif self.__exp1.get_type() == type.CHAR:

                    if self.__exp2.get_type() in (type.CHAR, type.STRING):
                        self.__type = type.STRING
                        return str(left) + str(right)
                    else: 
                        return Error("Semantic", f"The type: {self.__exp2.get_type().name} cannot be operated whit type: CHAR", self.row, self.column)
                
                elif self.__exp1.get_type() == type.STRING:

                    if self.__exp2.get_type() in (type.INTEGGER, type.FLOAT, type.CHAR, type.STRING, type.BOOLEAN):
                        self.__type = type.STRING
                        return str(left) + str(right)
                    else: 
                        return Error("Semantic", f"The type: {self.__exp2.get_type().name} cannot be operated whit type: STRING", self.row, self.column)
                else:
                    return Error("Semantic", f"The type: {self.__exp1.get_type().name} cannot be operated whit operator: +", self.row, self.column)

            if self.__operator == Arithmetic_Operator.SUBSTRACTION:

                if self.__exp1.get_type() == type.INTEGGER:

                    if self.__exp2.get_type() == type.INTEGGER:
                        self.__type = type.INTEGGER
                        return int(left) - int(right)
                    elif self.__exp2.get_type() == type.FLOAT:
                        self.__type = type.FLOAT
                        return float(left) - float(right)
                    elif self.__exp2.get_type() == type.BOOLEAN:
                        self.__type = type.INTEGGER
                        return int(left) - int(self.__bolean[right])
                    else:   
                        return Error("Semantic", f"The type: {self.__exp2.get_type().name} cannot be operated whit type: INTEGGER", self.row, self.column)

                elif self.__exp1.get_type() == type.FLOAT:
                    
                    if self.__exp2.get_type() in (type.INTEGGER, type.FLOAT):
                        self.__type = type.FLOAT
                        return float(left) - float(right)
                    elif self.__exp2.get_type() == type.BOOLEAN:
                        self.__type = type.FLOAT
                        return float(left) - float(self.__bolean[right])
                    else:   
                        return Error("Semantic", f"The type: {self.__exp2.get_type().name} cannot be operated whit type: FLOAT", self.row, self.column)
                
                elif self.__exp1.get_type() == type.BOOLEAN:

                    if self.__exp2.get_type() == type.INTEGGER:
                        self.__type = type.INTEGGER
                        return int(self.__bolean[left]) - int(right)
                    elif self.__exp2.get_type() == type.FLOAT:
                        self.__type = type.FLOAT
                        return float(self.__bolean[left]) - float(right)
                    elif self.__exp2.get_type() == type.BOOLEAN:
                        self.__type = type.INTEGGER
                        return float(self.__bolean[left]) - float(self.__bolean[right])
                    else:   
                        return Error("Semantic", f"The type: {self.__exp2.get_type().name} cannot be operated whit type: BOOLEAN", self.row, self.column)
                else:
                    return Error("Semantic", f"The type: {self.__exp1.get_type().name} cannot be operated whit operator: -", self.row, self.column)
        
            elif self.__operator == Arithmetic_Operator.MULTIPLICATION:

                if self.__exp1.get_type() == type.INTEGGER:

                    if self.__exp2.get_type() == type.INTEGGER:
                        self.__type = type.INTEGGER
                        return int(left) * int(right)
                    elif self.__exp2.get_type() == type.FLOAT:
                        self.__type = type.FLOAT
                        return float(left) * float(right)
                    else:   
                        return Error("Semantic", f"The type: {self.__exp2.get_type().name} cannot be operated whit type: INTEGGER", self.row, self.column)

                elif self.__exp1.get_type() == type.FLOAT:
                    
                    if self.__exp2.get_type() in (type.INTEGGER, type.FLOAT):
                        self.__type = type.FLOAT
                        return float(left) * float(right)
                    else:
                        return Error("Semantic", f"The type: {self.__exp2.get_type().name} cannot be operated whit type: FLOAT", self.row, self.column)
                else:
                    return Error("Semantic", f"The type: {self.__exp1.get_type().name} cannot be operated whit operator: *", self.row, self.column)
            
            elif self.__operator == Arithmetic_Operator.POWER:

                if self.__exp1.get_type() == type.INTEGGER:

                    if self.__exp2.get_type() == type.INTEGGER:
                        self.__type = type.INTEGGER
                        return int(left) ** int(right)
                    elif self.__exp2.get_type() == type.FLOAT:
                        self.__type = type.FLOAT
                        return float(left) ** float(right)
                    else:   
                        return Error("Semantic", f"The type: {self.__exp2.get_type().name} cannot be operated whit type: INTEGGER", self.row, self.column)

                elif self.__exp1.get_type() == type.FLOAT:
                    
                    if self.__exp2.get_type() in (type.INTEGGER, type.FLOAT):
                        self.__type = type.FLOAT
                        return float(left) ** float(right)
                    else:
                        return Error("Semantic", f"The type: {self.__exp2.get_type().name} cannot be operated whit type: FLOAT", self.row, self.column)
                else:
                    return Error("Semantic", f"The type: {self.__exp1.get_type().name} cannot be operated whit operator: **", self.row, self.column)

            elif self.__operator == Arithmetic_Operator.DIVISION:

                if int(right) != 0:
                    if self.__exp1.get_type() in (type.INTEGGER, type.FLOAT):

                        if self.__exp2.get_type() in (type.INTEGGER, type.FLOAT):
                            self.__type = type.FLOAT
                            return float(left) / float(right)
                        else:   
                            return Error("Semantic", f"The type: {self.__exp2.get_type().name} cannot be operated whit type: {self.__exp1.get_type().name}", self.row, self.column)
                    else: 
                        return Error("Semantic", f"The type: {self.__exp1.get_type().name} cannot be operated whit operator: /", self.row, self.column)
                else:
                    return Error("Semantic", "Cannot divide by zero", self.row, self.column)
            
            elif self.__operator == Arithmetic_Operator.MODULS:

                if int(right) != 0:
                    if self.__exp1.get_type() in (type.INTEGGER, type.FLOAT):

                        if self.__exp2.get_type() in (type.INTEGGER, type.FLOAT):
                            self.__type = type.FLOAT
                            return float(left) % float(right)
                        else:   
                            return Error("Semantic", f"The type: {self.__exp2.get_type().name} cannot be operated whit type: {self.__exp1.get_type().name}", self.row, self.column)
                    else: 
                        return Error("Semantic", f"The type: {self.__exp1.get_type().name} cannot be operated whit operator: %", self.row, self.column)
                else:
                    return Error("Semantic", "Cannot divide by zero", self.row, self.column)
        else:
            
            if self.__exp1.get_type() == type.INTEGGER:
                self.__type = type.INTEGGER
                return -int(left)
            elif self.__exp1.get_type() == type.FLOAT:
                self.__type = type.FLOAT
                return -float(left)
            else:
                return Error("Semantic", f"The type: {self.__exp1.get_type().name} cannot be operated whit operator: -", self.row, self.column)
            
    def get_type(self):
        return self.__type
