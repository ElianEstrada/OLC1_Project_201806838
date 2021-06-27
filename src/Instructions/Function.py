from src.Instructions.Continue import Coninue
from src.Instructions.Return import Return
from src.Abstract.Instruction import Instruction
from src.SymbolTable.Errors import Error
from src.SymbolTable.Type import type
from src.Instructions.Break import Break
from src.SymbolTable.SymbolTable import SymbolTable


class Function(Instruction):

    def __init__(self, name, params, instructions, row, column):
        self.__name = name.lower()
        self.__params = params
        self.__instructions = instructions
        self.__type = type.NULL
        self.row = row
        self.column = column

    
    def interpret(self, tree, table):

        new_table = SymbolTable(table)

        for instruction in self.__instructions:
            value = instruction.interpret(tree, new_table)

            if isinstance(value, Error):
                tree.get_errors().append(value)
                tree.update_console(value)

            if isinstance(value, Break):
                error = Error("Semantic", "Instruction Break out of loop", instruction.row, instruction.column)
                tree.get_errors().append(error)
                tree.get_update(error)
            
            if isinstance(value, Coninue):
                error = Error("Semantic", "Instruction Continue out of loop", instruction.row, instruction.column)
                tree.get_errors().append(error)
                tree.get_update(error)

            if isinstance(value, Return):
                self.__type = value.get_type()
                return value.get_result()
            
        
        return None


    def get_type(self):
        return self.__type

    def get_name(self):
        return self.__name

    def get_params(self):
        return self.__params
            


