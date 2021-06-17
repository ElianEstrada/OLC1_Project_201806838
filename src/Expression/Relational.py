from src.Abstract.Instruction import Instruction
from src.SymbolTable.Type import type, Relational_Operators
from src.SymbolTable.Errors import Error

class Relational(Instruction):

    def __init__(self, exp1, exp2, operator, row, column):
        self.__operator = operator
        self.__exp1 = exp1
        self.__exp2 = exp2
        self.row = row
        self.column = column
        self.__type = type.BOOLEAN
        self.__bolean = {
            "true": True,
            "false": False
        }

    def interpret(self, tree, table):

        
        if self.__exp2 != None and self.__exp1 != None:

            left = self.__exp1.interpret(tree, table)

            if isinstance(left, Error):
                return left
            
            right = self.__exp2.interpret(tree, table)

            if isinstance(right, Error):
                return right

            if self.__operator in (Relational_Operators.EQUAL, Relational_Operators.UNEQUAL):

                if self.__operator == Relational_Operators.EQUAL:
                    operator = '=='
                else:
                    operator = '=!'

                if self.__exp1.get_type() in (type.INTEGGER, type.FLOAT):

                    if self.__exp2.get_type() in (type.INTEGGER, type.FLOAT):
                        return self.to_lower(left, right, operator)
                    elif self.__exp2.get_type() == type.STRING:
                        return self.to_lower(str(left), right, operator)
                    else: 
                        return Error("Semantic", f"The type: {self.__exp2.get_type().name} cannot be operated whit type: {self.__exp1.get_type().name}", self.row, self.column)
                elif self.__exp1.get_type() == type.BOOLEAN:

                    if self.__exp2.get_type() == type.BOOLEAN:
                        return self.to_lower(self.__bolean[left], self.__bolean[right], operator)
                    elif self.__exp2.get_type() == type.STRING: 
                        return self.to_lower(left, right.lower(), operator)
                    else: 
                        return Error("Semantic", f"The type: {self.__exp2.get_type().name} cannot be operated whit type: BOOLEAN", self.row, self.column)
                elif self.__exp1.get_type() == type.CHAR:

                    if self.__exp2.get_type() == type.CHAR:
                        return self.to_lower(left, right, operator)
                    else: 
                        return Error("Semantic", f"The type: {self.__exp2.get_type().name} cannot be operated whit type: CHAR", self.row, self.column)
                elif self.__exp1.get_type() == type.STRING:

                    if self.__exp2.get_type() in (type.INTEGGER, type.FLOAT):
                        return self.to_lower(left, str(right), operator)
                    elif self.__exp2.get_type() == type.BOOLEAN:
                        return self.to_lower(left.lower(), right, operator)
                    elif self.__exp2.get_type() == type.STRING:
                        return self.to_lower(left, right, operator)
                    else:
                        return Error("Semantic", f"The type: {self.__exp2.get_type().name} cannot be operated whit type: STRING", self.row, self.column)
                else: 
                    return Error("Semantic", f"The type: {self.__exp1.get_type().name} cannot be operated whit operator: {operator}", self.row, self.column)
                    
            elif self.__operator in (Relational_Operators.GREATER, Relational_Operators.GREATEREQUAL, Relational_Operators.LESS, Relational_Operators.LESSEQUAL):

                if self.__operator == Relational_Operators.GREATER:
                    operator = '>'
                elif self.__operator == Relational_Operators.GREATEREQUAL:
                    operator = '>='
                elif self.__operator == Relational_Operators.LESS:
                    operator = '<'
                else: 
                    operator = '<='

                if self.__exp1.get_type() in (type.INTEGGER, type.FLOAT):

                    if self.__exp2.get_type() in (type.INTEGGER, type.FLOAT):
                        return self.to_lower(left, right, operator)
                    else:
                        return Error("Semantic", f"The type: {self.__exp2.get_type().name} cannot be operated whit type: {self.__exp1.get_type().name}", self.row, self.column)
                elif self.__exp1.get_type() == type.BOOLEAN:

                    if self.__exp2.get_type() == type.BOOLEAN:
                        return self.to_lower(self.__bolean[left], self.__bolean[right], operator)
                    else:
                        return Error("Semantic", f"The type: {self.__exp2.get_type().name} cannot be operated whit type: BOOLEAN", self.row, self.column)
                else:
                    return Error("Semantic", f"The type: {self.__exp1.get_type().name} cannot be operated whit operator: {operator}", self.row, self.column)
            

        else: 
            return Error("Semantic", "Expression Expected", self.row, self.column)



    def to_lower(self, left, right, operator):

        if operator == '==':
            return str(left == right).lower()
        elif operator == '=!':
            return str(left != right).lower()
        elif operator == '<':
            return str(left < right).lower()
        elif operator == '<=':
            return str(left <= right).lower()
        elif operator == '>':
            return str(left > right).lower()
        elif operator == '>=':
            return str(left >= right).lower()


    def get_type(self):
        return self.__type