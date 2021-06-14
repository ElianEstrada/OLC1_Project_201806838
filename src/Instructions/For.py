from src.SymbolTable.SymbolTable import SymbolTable
from src.Abstract.Instruction import Instruction
from src.SymbolTable.Type import type
from src.SymbolTable.Errors import Error


class For(Instruction):

    def __init__(self, init, condition, advance, instructions, row, column):
        self.__init = init
        self.__condition = condition
        self.__advance = advance
        self.__instructions = instructions
        self.row = row
        self.column = column

    
    def interpret(self, tree, table):

        init = self.__init.interpret(tree, table)

        if isinstance(init, Error):
            return init

        while True:

            flag = self.__condition.interpret(tree, table)

            if isinstance(flag, Error):
                return flag

            if self.__condition.get_type() == type.BOOLEAN:
                if flag == "true":

                    new_table = SymbolTable(table)

                    for item in self.__instructions:
                        instruction = item.interpret(tree, new_table)

                        if isinstance(instruction, Error):
                            tree.get_errors().append(instruction)
                            tree.update_console(instruction)

                    advance = self.__advance.interpret(tree, new_table)

                    if isinstance(advance, Error):
                        return advance
                else:
                    break
            else:
                return Error("Semantic", f"Expect a Boolean type expression not of type {self.__exp.get_typ().name}", self.row, self.column)
