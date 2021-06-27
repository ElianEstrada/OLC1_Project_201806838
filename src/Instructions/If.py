from src.Instructions.Break import Break
from src.Instructions.Continue import Continue
from src.SymbolTable.SymbolTable import SymbolTable
from src.SymbolTable.Errors import Error
from src.Instructions.Return import Return
from src.Abstract.Instruction import Instruction
from src.SymbolTable.Type import type

class If(Instruction):

    def __init__(self, exp, instructions, else_instruction, else_if, row, column):
        self.__exp = exp
        self.__instructions = instructions
        self.__else_instructions = else_instruction
        self.__else_if = else_if
        self.row = row
        self.column = column

    def interpret(self, tree, table):

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

                    if isinstance(instruction, Continue):
                        return instruction

                    if isinstance(instruction, Break):
                        return instruction

                    if isinstance(instruction, Return):
                        return instruction
            else:
                if self.__else_instructions != None:

                    new_table = SymbolTable(table)
                    for item in self.__else_instructions:
                        instruction_else = item.interpret(tree, new_table)

                        if isinstance(instruction_else, Error):
                            tree.get_errors().append(instruction_else)
                            tree.update_console(instruction_else)

                        if isinstance(instruction_else, Continue):
                            return instruction_else  

                        if isinstance(instruction_else, Break):
                            return instruction_else

                        if isinstance(instruction_else, Return):
                            return instruction_else

                elif self.__else_if != None:

                    result = self.__else_if.interpret(tree, table)

                    if isinstance(result, Error):
                        return result

                    if isinstance(result, Return):
                        return result

        else: 
            return Error("Semantic", f"Expect a Boolean type expression not of type {self.__exp.get_typ().name}", self.row, self.column) 


                
