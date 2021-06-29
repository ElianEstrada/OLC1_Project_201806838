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

        list_positions = []
        value_positions = 1
        for pos in self.__position:


            position = pos.interpret(tree, table)

            if isinstance(position, Error):
                return position

            value_positions *= position

            list_positions.append(position)

        symbol = table.get_table(self.__name)

        if symbol == None:
            return Error("Semantic", f"The id: {self.__name} doesn't exist in current context", self.row, self.column)

        if value_positions <= len(symbol.get_value().get_list_value()) - 1:

            if len(list_positions) == 1:
                real_position = list_positions[0]
            else: 
                real_position = self.lexico_map(list_positions, symbol.get_value().get_expression()[1:], tree, table)

            if self.__expression == None:
                

                    value = symbol.get_value().get_list_value()[real_position].interpret(tree, table)

                    if isinstance(value, Error):
                        return value

                    self.__type = symbol.get_value().get_list_value()[real_position].get_type()

                    return value
                
                

            else:
                value = self.__expression.interpret(tree, table)

                if self.__expression.get_type() == symbol.get_value().get_type():

                    #list_value = []        
                    count = 0

                    while count < len(symbol.get_value().get_list_value()):

                        if count == real_position: 
                            symbol.get_value().get_list_value()[real_position] = Primitive(self.__expression.get_type(), value, self.row, self.column)

                        count += 1

                    new_symbol = Symbol(self.__name, type.ARRAY, self.row, self.column, symbol.get_value())

                    result = table.update_table(new_symbol)

                    if isinstance(result, Error):
                        return result
                
                else: 
                    return Error("Semantic", f"The type: {self.__expression.get_type().name} can not assignated of type: {symbol.get_sub_type().name}", self.row, self.column)
        else:
                    return Error("Semantic", f"{position} out to index array", self.row, self.column)

        return None
    
    def get_type(self):
        return self.__type

    def lexico_map(self, positions, max_index, tree, table):

        if [] not in (positions, max_index):
            return positions[0] * max_index[0].interpret(tree, table) + self.lexico_map(positions[1:], max_index[1:], tree, table)
        
        return 0

