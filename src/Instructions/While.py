from src.Abstract.Instruction import Instruction
from src.Instructions.Break import Break
from src.SymbolTable.SymbolTable import SymbolTable
from src.SymbolTable.Errors import Error
from src.SymbolTable.Type import type


class While(Instruction):

    def __init__(self, exp, instructions, row, column):
        self.__exp = exp
        self.__instructions = instructions
        self.row = row
        self.column = column

    def interpret(self, tree, table):

        while True:
            flag = self.__exp.interpret(tree, table)

            if isinstance(flag, Error):
                return flag

            if self.__exp.get_type() == type.BOOLEAN:
                
                if flag == "true":

                    new_table = SymbolTable(table)

                    for item in self.__instructions:
                        instruction = item.interpret(tree, new_table)

                        if isinstance(instruction, Error):
                            tree.get_errors().append(instruction)
                            tree.update_console(instruction)

                        if isinstance(instruction, Break):
                            return None
                else: 
                    break
            else: 
                return Error("Semantic", f"Expect a Boolean type expression not of type {self.__exp.get_typ().name}", self.row, self.column)
