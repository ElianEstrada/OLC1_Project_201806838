from src.Abstract.Instruction import Instruction
from src.SymbolTable.Type import type
from src.SymbolTable.Errors import Error
from src.Expression.Primitive import Primitive
from src.SymbolTable.Symbol import Symbol

class Array(Instruction):

    def __init__(self, type_init, name, type_assig, expression, list_expression, row, column):
        self.__type_init = type_init
        self.__name = name.lower()
        self.__type_assig = type_assig
        self.__expression = expression
        self.__list_expression = list_expression
        self.__type = type.NULL
        self.row = row
        self.column = column


    def interpret(self, tree, table):

        symbol = ""

        if None not in (self.__type_assig, self.__expression):
            if self.__type_assig == self.__type_init:
                value = self.__expression.interpret(tree, table)

                if isinstance(value, Error):
                    return value
                
                if self.__expression.get_type() != type.INTEGGER:
                    return Error("Semantic", f"The type: {self.__expression.get_type().name} for expression is invalid, must be of type INTEGGER", self.row, self.count)

                list_value = []        
                count = 0

                while count < value:
                    primitive = Primitive(type.NULL, 'null', self.row, self.column)

                    list_value.append(primitive)

                    count += 1

                symbol = Symbol(self.__name, type.ARRAY, self.row, self.column, list_value, self.__type_assig)


            else:
                return Error("Semantic", f"The type: {self.__type_assig.name} can not assigned to type: {self.__type_init.name}", self.row, self.column)

            result = table.set_table(symbol)

            if isinstance(result, Error):
                return result

            return None

    def get_type(self):
        return self.__type_init
