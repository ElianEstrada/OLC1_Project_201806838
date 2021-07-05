from src.Instructions.Function import Function
from src.Abstract.Ast_Node import Ast_Node
from src.Instructions.Continue import Continue
from src.Abstract.Instruction import Instruction
from src.SymbolTable.Errors import Error
from src.Instructions.Break import Break
from src.Instructions.Print import Print
from src.Instructions.Assignment import Assignment
from src.Instructions.Declaration import Declaration
from src.SymbolTable.Type import type
from src.SymbolTable.SymbolTable import SymbolTable

import tkinter.messagebox as msg

class Main(Instruction):

    def __init__(self, instructions, row, column):
        self.__instructions = instructions
        self.row = row
        self.column = column

    def interpret(self, tree, table):
        
        new_table = SymbolTable(table, "Method_Main", table.get_widget())

        tree.set_symbol_table(new_table)

        for item in self.__instructions:

            if isinstance(item, Function):
                error = Error("Semantic", "The Instruction Func don't be into of method main", item.row, item.column)
                tree.get_errors().append(error)
                tree.update_console(error)
                continue
            
            instruction = item.interpret(tree, new_table)

            if isinstance(instruction, Error):
                tree.get_errors().append(instruction)
                tree.update_console(instruction)
                continue
            
            if isinstance(instruction, Break):
                error = Error("Semantic", "The Instruction BREAK is loop or switch instruction", instruction.row, instruction.column)
                tree.get_errors().append(error)
                tree.update_console(error)
                continue

            if isinstance(instruction, Continue):
                error = Error("Semantic", "The Instruction Continue is loop instruction", instruction.row, instruction.column)
                tree.get_errors().append(error)
                tree.update_console(error)
                continue

            if tree.get_debugg():

                tree.get_input_text().tag_add("debugg", f"{item.row}.0", f"{item.row + 1}.0")
                tree.get_input_text().see(f"{item.row}.0")
                tree.get_table().delete(*tree.get_table().get_children())
                if isinstance(item, Print):
                    tree.get_output_text().delete("1.0", "end")
                    tree.get_output_text().insert('insert', tree.get_console())
                    tree.get_output_text().see('end')
                count = 0
                for variable in new_table.get_variables():
                    if variable.get_type() == type.ARRAY:
                        tree.get_table().insert('', "end", text=variable.get_id(), values=(variable.get_type().name, variable.get_value().get_type().name, variable.get_environment(), variable.get_value(), variable.get_row(), variable.get_column()))
                    else:
                        tree.get_table().insert('', "end", text=variable.get_id(), values=("VARIABLE", variable.get_type().name, variable.get_environment(), variable.get_value(), variable.get_row(), variable.get_column()))
                if isinstance(item, Assignment):
                    while count < len(tree.get_table().get_children()) - 1:
                        date = tree.get_table().item(tree.get_table().get_children()[count])
                        if date['text'] == item.get_id():
                            break
                        count += 1
                if isinstance(item, Declaration):
                    count = -1
                if len(tree.get_table().get_children()) != 0:
                    tree.get_table().see(tree.get_table().get_children()[count])
                var = msg.askyesno(title="Debugger", message="Continue?...")
                tree.get_input_text().tag_remove("debugg", f"{item.row}.0", f"{item.row + 1}.0")
                if var:
                    continue
                else:
                    tree.set_debugg(False)

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