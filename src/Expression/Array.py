from src.Abstract.Instruction import Instruction
from src.SymbolTable.Type import type
from src.SymbolTable.Errors import Error
from src.Expression.Primitive import Primitive
from src.SymbolTable.Symbol import Symbol

class Array(Instruction):

    def __init__(self, type_init, len_init, name, type_assig, expression, list_expression, row, column):
        self.__type_init = type_init
        self.__name = name.lower()
        self.__type_assig = type_assig
        self.__len_init = len(len_init)
        self.__expression = expression
        self.__list_value = []
        self.__list_expression = list_expression
        self.__type = type.NULL
        self.row = row
        self.column = column


    def interpret(self, tree, table):

        symbol = ""

        if None not in (self.__type_assig, self.__expression):
            if self.__type_assig == self.__type_init:

                if self.__len_init == len(self.__expression):
                    len_array = 1

                    for expression in self.__expression:

                        value = expression.interpret(tree, table)

                        if isinstance(value, Error):
                            return value
                        
                        if expression.get_type() != type.INTEGGER:
                            return Error("Semantic", f"The type: {expression.get_type().name} for expression is invalid, must be of type INTEGGER", self.row, self.count)

                        len_array *= value

                    list_value = []        
                    count = 0

                    while count < len_array:
                        primitive = Primitive(type.NULL, 'null', self.row, self.column)

                        list_value.append(primitive)

                        count += 1

                    self.__list_value = list_value

                    symbol = Symbol(self.__name, type.ARRAY, self.row, self.column, self)

                else: 
                    return Error("Semantic", f"The number of dimensions is wrong: {self.__len_init} is not equal of {len(self.__expression)}", self.row, self.column)    

            else:
                return Error("Semantic", f"The type: {self.__type_assig.name} can not assigned to type: {self.__type_init.name}", self.row, self.column)

            result = table.set_table(symbol)

            if isinstance(result, Error):
                return result

            return None

    def get_type(self):
        return self.__type_init

    def get_expression(self):
        return self.__expression

    def get_list_expression(self):
        return self.__list_expression

    def get_list_value(self):
        return self.__list_value
