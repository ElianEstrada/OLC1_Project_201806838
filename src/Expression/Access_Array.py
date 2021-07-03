from src.Abstract.Ast_Node import Ast_Node
from src.Abstract.Instruction import Instruction
from src.Expression.Array import Array
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
        self.__value = None
        self.row = row
        self.column = column


    def interpret(self, tree, table):

        list_positions = []
        value_positions = 1

        if self.__position == []:
            symbol = table.get_table(self.__name)

            if symbol == None:
                return Error("Semantic", f"The id: {self.__name} doesn't exist in current context", self.row, self.column)

            symbol2 = table.get_table(self.__expression)

            if symbol2 == None:
                return Error("Semantic", f"The id: {self.__expression} doesn't exist in current context", self.row, self.column)

            if not isinstance(symbol, Array):
                return Error("Semantic", f"The id: {self.__name} must be an array", self.row, self.column)

            if not isinstance(symbol2, Array):
                return Error("Semantic", f"The id: {self.__expression} must be an array", self.row, self.column)
            
            new_symbol = Symbol(self.__name, type.ARRAY, self.row, self.column, symbol2.get_value())

            result = table.update_table(new_symbol)

            if isinstance(result, Error):
                return result

            return None
            

        for pos in self.__position:


            position = pos.interpret(tree, table)

            if isinstance(position, Error):
                return position

            if pos.get_type() != type.INTEGGER or position < 0:
                return Error("Semantic", f"The expression is invalid, must be of type INTEGGER", self.row, self.column)

            value_positions *= position

            list_positions.append(position)

        symbol = table.get_table(self.__name)

        if symbol == None:
            return Error("Semantic", f"The id: {self.__name} doesn't exist in current context", self.row, self.column)

        if len(list_positions) != symbol.get_value().get_len():
            return Error("Semantic", f"{symbol.get_value().get_len()} positions were expected and only {len(list_positions)} came", self.row, self.column)

        if symbol.get_value().get_list_expression() == []:

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
                        self.__value = value
                        return value

                else:
                    value = self.__expression.interpret(tree, table)

                    if self.__expression.get_type() == symbol.get_value().get_type():

                        #list_value = []        

                        symbol.get_value().get_list_value()[real_position] = Primitive(self.__expression.get_type(), value, self.row, self.column)

                        new_symbol = Symbol(self.__name, type.ARRAY, self.row, self.column, symbol.get_value())

                        result = table.update_table(new_symbol)

                        if isinstance(result, Error):
                            return result
                    
                    else: 
                        return Error("Semantic", f"The type: {self.__expression.get_type().name} can not assignated of type: {symbol.get_type().name}", self.row, self.column)
            else:
                return Error("Semantic", f"{position} out to index array", self.row, self.column)

        else:

            if self.__expression == None:
                value = self.value_position(list_positions, symbol.get_value().get_list_value(), tree, table)

                if isinstance(value, Error):
                    return value

                self.__type = symbol.get_value().get_type()
                self.__value = value
                return value

            else: 
                value = self.__expression.interpret(tree, table)

                symbol.get_value().set_list_value(self.assign_value(list_positions, symbol.get_value().get_list_value(), Primitive(self.__expression.get_type(), value, self.row, self.column)))

                new_symbol = Symbol(self.__name, type.ARRAY, self.row, self.column, symbol.get_value())

                result = table.update_table(new_symbol)

                if isinstance(result, Error):
                    return result

        return None

    def get_node(self):
        node = Ast_Node("Acces Array")

        node.add_child(self.__name)

        positions = Ast_Node("Expressions Array")

        for exp in self.__position:
            positions.add_child("[")
            positions.add_childs_node(exp.get_node())
            positions.add_child("]")

        node.add_childs_node(positions)

        if self.__expression != None:
            node.add_child("=")
            node.add_childs_node(self.__expression.get_node())

        return node
    
    def get_type(self):
        return self.__type

    def lexico_map(self, positions, max_index, tree, table):

        if [] not in (positions, max_index):
            return positions[0] * max_index[0].interpret(tree, table) + self.lexico_map(positions[1:], max_index[1:], tree, table)
        
        return 0

    def value_position(self, positions, list_values, tree, table):
        
        if positions != []:
            try: 
                return self.value_position(positions[1:], list_values[positions[0]], tree, table)
            except IndexError:
                return Error("Semantic", f"{positions[0]} out to index array", self.row, self.column)
        
        return list_values.interpret(tree, table)

    def assign_value(self, positions, list_values, value, flag = False, flag2 = True):

        expressions = []

        if isinstance(list_values, list):
            
            if flag:
                flag2 = True

            if flag2: 
                count = 0
            else: 
                count = 100

            for item in list_values:
                if len(positions) != 0 and positions[0] == count:
                    flag = True
                    flag2 = False
                    positions.pop(0)
                else:
                    flag = False
                    flag2 = False
                expressions.append(self.assign_value(positions, item, value, flag, flag2))
                #positions.pop(0)
                count += 1

        else: 
            if flag:
                return value
            
            return list_values

        return expressions

    def __str__(self):
        return str(self.__value)