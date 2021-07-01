from src.SymbolTable.SymbolTable import SymbolTable
from src.SymbolTable.Symbol import Symbol
from src.Abstract.Instruction import Instruction
from src.SymbolTable.Type import type
from src.SymbolTable.Errors import Error

import copy


class Call(Instruction):

    def __init__(self, name, params, row, column):
        self.__name = name.lower()
        self.__params = params
        self.__type = None
        self.row = row
        self.column = column

    def interpret(self, tree, table):
        ob_function = tree.get_function(self.__name)

        if ob_function == None:
            return Error("Semantic", f"The function whit the name: {self.__name} doesn't exits", self.row, self.column)

        new_table = SymbolTable(tree.get_global_table())

        if len(ob_function.get_params()) == len(self.__params): 

            count = 0
            for expression in self.__params:
                value_expression = expression.interpret(tree, table)

                if isinstance(value_expression, Error):
                    return value_expression


                if str(ob_function.get_params()[count]['name']).lower() in ('length##param1', 'round##param1', 'truncate##param1', 'type_of##param1'):
                    
                    symbol = Symbol(str(ob_function.get_params()[count]['name']).lower(), expression.get_type(), self.row, self.column, value_expression)
                    table_result = new_table.set_table(symbol)

                    if isinstance(table_result, Error):
                        return table_result

                    break

                if ob_function.get_params()[count]['type'] == expression.get_type():

                    if expression.get_type() == type.ARRAY:

                        if len(ob_function.get_params()[count]['len']) != value_expression.get_len():
                            return Error("Semantic", f"the size of dimensions is: {len(ob_function.get_params()[count]['len'])} not {value_expression.get_len()}", self.row, self.column)

                        if ob_function.get_params()[count]['sub_type'] != value_expression.get_type():
                            return Error("Semantic", f"The type: {value_expression.get_type().name} is different to param the type: {ob_function.get_params()[count]['sub_type']}", self.row, self.column)

                        value_expression = copy.copy(value_expression)
                        value_expression.set_list_value(copy.copy(value_expression.get_list_value()))

                    symbol = Symbol(str(ob_function.get_params()[count]['name']).lower(), expression.get_type(), self.row, self.column, value_expression)
                    table_result = new_table.set_table(symbol)

                    if isinstance(table_result, Error):
                        return table_result
                else: 
                    return Error("Semantic", f"The type: {expression.get_type().name} is different to param the type: {ob_function.get_params()[count]['type']}", self.row, self.column)

                count += 1
        
        value = ob_function.interpret(tree, new_table)

        if isinstance(value, Error):
            return value

        self.__type = ob_function.get_type()

        return value

    def get_type(self):
        return self.__type