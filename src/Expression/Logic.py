from src.Abstract.Instruction import Instruction
from src.SymbolTable.Errors import Error
from src.SymbolTable.Type import type, Logical_Operators


class Logic(Instruction):

    def __init__(self, exp1, exp2, operator, row, column):
        self.__operator = operator
        self.__exp1 = exp1
        self.__exp2 = exp2
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

            if self.__operator == Logical_Operators.AND:
                return str(self.__bolean[left] and self.__bolean[right]).lower()
            elif self.__operator == Logical_Operators.OR:
                return str(self.__bolean[left] or self.__bolean[right]).lower()

        else:
            return str(not self.__bolean[left]).lower()

    def get_type(self):
        return self.__type