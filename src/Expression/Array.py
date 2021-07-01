from src.Abstract.Instruction import Instruction
from src.SymbolTable.Type import type
from src.SymbolTable.Errors import Error
from src.Expression.Primitive import Primitive
from src.SymbolTable.Symbol import Symbol

class Array(Instruction):

    def __init__(self, type_init, len_init, name, type_assig, expression, list_expression, row, column, id_array = None):
        self.__type_init = type_init
        self.__name = name.lower()
        self.__type_assig = type_assig
        self.__len_init = len(len_init)
        self.__expression = expression
        self.__list_value = []
        self.__list_expression = list_expression
        self.__type = type.NULL
        self.__id_array = id_array
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
                        
                        if expression.get_type() != type.INTEGGER or value < 0:
                            return Error("Semantic", f"The expression is invalid, must be of type INTEGGER", self.row, self.column)

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

        elif self.__list_expression != []: 
            
            #len_array = self.calc_positions(self.__list_expression) 

            #list_aux = self.get_list(self.__list_expression, tree, table)

            # if isinstance(list_aux, Error):
            #     return list_aux

            #list_values = []

            #for item in list_aux:
            #    if self.__type_init == type.INTEGGER:
            #        primitive = Primitive(type.INTEGGER, int(item), self.row, self.column)
            #    elif self.__type_init == type.FLOAT:
            #        primitive = Primitive(type.FLOAT, float(item), self.row, self.column)
            #    else:
            #primitive = Primitive(self.__type_init, item, self.row, self.column)

            #    list_values.append(primitive)

            self.__list_value = self.__list_expression

            symbol = Symbol(self.__name, type.ARRAY, self.row, self.column, self)

        else:

            value = self.__id_array.interpret(tree, table)

            if isinstance(value, Error):
                return value

            if not isinstance(value, Array):
                return Error("Semantic", "Assignated only arrays", self.row, self.column)

            if self.__len_init != value.get_len():
                return Error("Semantic", f"The dimension: {value.get_len()} can not assigned to array of dimension: {self.__len_init}", self.row, self.column)

            if self.__type_init != value.get_type():
                return Error("Semantic", f"The type: {value.get_type().name} can not assigned to array of type: {self.__type_init.name}", self.row, self.column)

            symbol = Symbol(self.__name, type.ARRAY, self.row, self.column, value)

        result = table.set_table(symbol)

        if isinstance(result, Error):
            return result

        return None


    def get_list(self, list_values, tree, table):

        expressions = ""

        if isinstance(list_values, list):

            for item in list_values:

                result = self.get_list(item, tree, table)

                if isinstance(result, Error):
                    return result

                expressions += result + ','

        else:

            if list_values.get_type() == self.__type_init:

                value = list_values.interpret(tree, table)

                if isinstance(value, Error):
                    return value

                return str(value)
            
            else: 
                return Error("Semantic", f"The type: {list_values.get_type().name} can not assigned to the type: {self.__type_init}", self.row, self.column)

        return expressions[:-1]

    def get_type(self):
        return self.__type_init

    def get_expression(self):
        return self.__expression

    def get_list_expression(self):
        return self.__list_expression

    def get_list_value(self):
        return self.__list_value

    def set_list_value(self, list_values):
        self.__list_value = list_values

    def get_len(self):
        return self.__len_init
