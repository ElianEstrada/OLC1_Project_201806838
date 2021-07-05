from src.Abstract.Ast_Node import Ast_Node
from src.Abstract.Instruction import Instruction
from src.SymbolTable.Symbol import Symbol
from src.SymbolTable.Errors import Error
from src.SymbolTable.Type import type

class Assignment(Instruction):

    def __init__(self, id, expression, row, column):
        self.__id = id.lower()
        self.__expression = expression
        self.row = row
        self.column = column

    
    def interpret(self, tree, table):
            
        value = self.__expression.interpret(tree, table)

        if isinstance(value, Error):
            return value

        if self.__expression.get_type() == type.ARRAY:

            symbol = table.get_table(self.__id)

            if isinstance(symbol, Error):
                return symbol

            if value.get_len() != symbol.get_value().get_len():
                return Error("Semantic", f"the size of dimensions is: {value.get_len()} not {symbol.get_value().get_len()}", self.row, self.column)

            if self.calc_positions(value.get_list_value()) != self.calc_positions(symbol.get_value().get_list_value()):
                return Error("Semantic", f"The number of positions is different, can not assigned", self.row, self.column)

            if value.get_type() != symbol.get_value().get_type():
                return Error("Semantic", f"The type: {value.get_type().name} can not assigned to the type: {symbol.get_value().get_type().name}", self.row, self.column)


        new_symbol = Symbol(self.__id, self.__expression.get_type(), self.row, self.column, value)
        #new_symbol.set_environment(table.get_name())
        result = table.update_table(new_symbol)

        if isinstance(result, Error):
            return result
        
        return None
            

    def get_node(self):
        node = Ast_Node("Assignment")
        node.add_child(self.__id)
        node.add_child("=")
        node.add_childs_node(self.__expression.get_node())

        return node


    def set_id(self, id):
        self.__id = id

    def get_id(self):
        return self.__id

    def set_expression(self, expression):
        self.__expression = expression
    
    def get_expression(self):
        return self.__expression

    def calc_positions(self, list_values):

        if isinstance(list_values, list):
            return len(list_values) * self.calc_positions(list_values[0])

        return 1