from src.Abstract.Ast_Node import Ast_Node
from src.Abstract.Instruction import Instruction
from src.SymbolTable.Errors import Error
from src.SymbolTable.Type import type, Logical_Operators


class Logic(Instruction):

    def __init__(self, exp1, exp2, operator, row, column):
        self.__operator = operator
        self.__exp1 = exp1
        self.__exp2 = exp2
        self.__value = None
        self.row = row
        self.column = column
        self.__type = type.BOOLEAN
        self.__bolean = {
            "true": True,
            "false": False
        }

    def interpret(self, tree, table):

        left = self.__exp1.interpret(tree, table)

        if isinstance(left, Error):
            return left

        if self.__exp2 != None:

            right = self.__exp2.interpret(tree, table)

            if isinstance(right, Error):
                return right

            if type.BOOLEAN in (self.__exp1.get_type(), self.__exp2.get_type()):


                if self.__operator == Logical_Operators.AND:
                    self.__value = str(self.__bolean[left] and self.__bolean[right]).lower()
                    return str(self.__bolean[left] and self.__bolean[right]).lower()
                elif self.__operator == Logical_Operators.OR:
                    self.__value = str(self.__bolean[left] or self.__bolean[right]).lower()
                    return str(self.__bolean[left] or self.__bolean[right]).lower()
            else: 
                return Error("Semantic", f"This operators only work whit type BOOLEAN", self.row, self.column)

        else:

            if type.BOOLEAN == self.__exp1.get_type():
                self.__value = str(not self.__bolean[left]).lower()
                return str(not self.__bolean[left]).lower()

            return Error("Semantic", f"The type: {self.__exp1.get_type().name} does not work whit operator !", self.row, self.column)

    def get_operator(self, operator):

        if operator == Logical_Operators.AND:
            return '&&'
        else:
            return '||'

    def get_node(self):
        node = Ast_Node("Expression Logic")

        if self.__exp2 != None:
            node.add_childs_node(self.__exp1.get_node())
            node.add_child(self.get_operator(self.__operator))
            node.add_childs_node(self.__exp2.get_node())
        else: 
            node.add_child("!")
            node.add_childs_node(self.__exp1.get_node())

        return node

    def get_type(self):
        return self.__type

    def __str__(self):
        return self.__value 