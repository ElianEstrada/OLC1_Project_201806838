from src.Abstract.Instruction import Instruction
from src.SymbolTable.Errors import Error
from src.Instructions.Break import Break
from src.SymbolTable.SymbolTable import SymbolTable


class Main(Instruction):

    def __init__(self, instructions, row, column):
        self.__instructions = instructions
        self.row = row
        self.column = column

    def interpret(self, tree, table):
        
        new_table = SymbolTable(table)

        for item in self.__instructions:
            instruction = item.interpret(tree, new_table)

            if isinstance(instruction, Error):
                tree.get_errors().append(instruction)
                tree.update_console(instruction)
            
            if isinstance(instruction, Break):
                error = Error("Semantic", "The Instruction BREAK is loop or switch instruction", instruction.row, instruction.column)
                tree.get_errors().append(error)
                tree.update_console(error)
