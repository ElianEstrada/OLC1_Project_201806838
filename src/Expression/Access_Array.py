from src.Abstract.Instruction import Instruction
from src.SymbolTable.Type import type
from src.SymbolTable.Errors import Error
from src.Expression.Primitive import Primitive
from src.SymbolTable.Symbol import Symbol


class Access_Array(Instruction):
    
    def __init__(self, name, position, expression, row, column):
        self.__name = name.lower()
        self.__position = position
        self.__expression = expression
        self.__type = type.NULL
        self.row = row
        self.column = column


    def interpret(self, tree, table):
        position = self.__position.interpret(tree, table)

        if isinstance(position, Error):
            return position

        symbol = table.get_table(self.__name)

        if symbol == None:
            return Error("Semantic", f"The id: {self.__name} doesn't exist in current context", self.row, self.column)

        if self.__expression == None:
            if position <= len(symbol.get_value()) - 1:

                value = symbol.get_value()[position].interpret(tree, table)

                if isinstance(value, Error):
                    return value

                self.__type = symbol.get_value()[position].get_type()

                return value
            
            else:
                return Error("Semantic", f"{position} out to index array", self.row, self.column)

        else:
            value = self.__expression.interpret(tree, table)

            if self.__expression.get_type() == symbol.get_sub_type():

                list_value = []        
                count = 0

                while count < len(symbol.get_value()):

                    if count == position: 
                        primitive = Primitive(self.__expression.get_type(), value, self.row, self.column)
                    else: 
                        primitive = Primitive(type.NULL, 'null', self.row, self.column)

                    list_value.append(primitive)

                    count += 1

                new_symbol = Symbol(self.__name, type.ARRAY, self.row, self.column, list_value)

                result = table.update_table(new_symbol)

                if isinstance(result, Error):
                    return result
        
        return None
    
    def get_type(self):
        return self.__type


