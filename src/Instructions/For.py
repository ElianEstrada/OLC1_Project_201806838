from src.SymbolTable.SymbolTable import SymbolTable
from src.Abstract.Instruction import Instruction
from src.Instructions.Break import Break
from src.Instructions.Return import Return
from src.Instructions.Declaration import Declaration
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


        if None not in (self.__init, self.__condition, self.__advance):
            new_table = None
            declar_flag = False
            if isinstance(self.__init, Declaration):
                new_table = SymbolTable(table)
                declar_flag = True
                init = self.__init.interpret(tree, new_table)
            else:
                init = self.__init.interpret(tree, table)

            if isinstance(init, Error):
                return init

            while True:

                if new_table == None:
                    flag = self.__condition.interpret(tree, table)
                else:
                    flag = self.__condition.interpret(tree, new_table)

                if isinstance(flag, Error):
                    return flag

                if self.__condition.get_type() == type.BOOLEAN:
                    if flag == "true":

                        if not declar_flag:
                            new_table = SymbolTable(table)
                        else:
                            new_table = SymbolTable(new_table)

                        if self.__instructions != None:
                            for item in self.__instructions:
                                instruction = item.interpret(tree, new_table)

                                if isinstance(instruction, Error):
                                    tree.get_errors().append(instruction)
                                    tree.update_console(instruction)
                                
                                if isinstance(instruction, Break):
                                    return None
                                
                                if isinstance(instruction, Return):
                                    return instruction

                        advance = self.__advance.interpret(tree, new_table)
                        
                        if isinstance(advance, Error):
                            return advance
                    else:
                        break
                else:
                    return Error("Semantic", f"Expect a Boolean type expression not of type {self.__exp.get_typ().name}", self.row, self.column)

            else:
                return Error("Semantic", "Expression Expected", self.row, self.column)
