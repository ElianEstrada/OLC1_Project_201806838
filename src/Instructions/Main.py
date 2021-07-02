from src.Abstract.Ast_Node import Ast_Node
from src.Instructions.Continue import Continue
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

            if isinstance(instruction, Continue):
                error = Error("Semantic", "The Instruction Continue is loop instruction", instruction.row, instruction.column)
                tree.get_errors().append(error)
                tree.update_console(error)


    def get_node(self):
        node = Ast_Node("Main")
        node.add_child("main")
        node.add_child("(")
        node.add_child(")")
        node.add_child("{")

        instructions = Ast_Node("Instructions")
        for inst in self.__instructions:
            instructions.add_childs_node(inst.get_node())
        node.add_childs_node(instructions)

        node.add_child("}")

        return node