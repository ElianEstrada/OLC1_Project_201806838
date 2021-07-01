from src.Abstract.Ast_Node import Ast_Node
from src.SymbolTable.Errors import Error
from src.Abstract.Instruction import Instruction
from src.Expression.Identifier import Identifier
from src.SymbolTable.Symbol import Symbol
from src.SymbolTable.Type import type, Arithmetic_Operator


class Int_Dec(Instruction):

    def __init__(self, exp, operator, row, column):
        self.__exp = exp
        self.__operator = operator
        self.__type = None
        self.row = row
        self.column = column

    
    def interpret(self, tree, table):
        
        if isinstance(self.__exp, Identifier):

            value = self.__exp.interpret(tree, table)

            if isinstance(value, Error):
                    return value

            if self.__exp.get_type() in (type.INTEGGER, type.FLOAT):
                
                if self.__operator == Arithmetic_Operator.INC:
                    symbol = Symbol(self.__exp.get_id(), self.__exp.get_type(), self.row, self.column, value + 1)
                elif self.__operator == Arithmetic_Operator.DEC:
                    symbol = Symbol(self.__exp.get_id(), self.__exp.get_type(), self.row, self.column, value - 1)

                result = table.update_table(symbol)

                if isinstance(result, Error):
                    return result
                
                self.__type = self.__exp.get_type()

                return symbol.get_value()
            else:
                return Error("Semantic", f"The type: {self.__exp.get_type().name} cannot be operated whit operator: {self.__operator.name}", self.row, self.column)
        else:
            return Error("Semantic", f"The operator: {self.__operator.name} can only be used on variables", self.row, self.column)

    def get_node(self):
        node = Ast_Node("Incremento_Decremento")

        node.add_childs_node(self.__exp.get_node())
        if self.__operator == Arithmetic_Operator.INC:
            node.add_child("++")
        else: 
            node.add_child("--")

        return node;

    def set_exp(self, exp):
        self.__exp = exp

    def get_exp(self):
        return self.__exp

    def get_type(self):
        return self.__type
