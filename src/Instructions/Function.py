from src.Abstract.Ast_Node import Ast_Node
from src.Instructions.Continue import Continue
from src.Instructions.Return import Return
from src.Abstract.Instruction import Instruction
from src.Instructions.Print import Print
from src.Instructions.Assignment import Assignment
from src.Instructions.Declaration import Declaration
from src.SymbolTable.Errors import Error
from src.SymbolTable.Type import type
from src.Instructions.Break import Break
from src.SymbolTable.SymbolTable import SymbolTable

import tkinter.messagebox as msg

class Function(Instruction):

    def __init__(self, name, params, instructions, row, column):
        self.name = name.lower()
        self.params = params
        self.instructions = instructions
        self.type = type.NULL
        self.row = row
        self.column = column

    
    def interpret(self, tree, table):

        new_table = SymbolTable(table, f"Function-{self.name}-{self.row}-{self.column}")

        for instruction in self.instructions:
            value = instruction.interpret(tree, new_table)

            if isinstance(value, Error):
                tree.get_errors().append(value)
                tree.update_console(value)

            if isinstance(value, Break):
                error = Error("Semantic", "Instruction Break out of loop", instruction.row, instruction.column)
                tree.get_errors().append(error)
                tree.get_update(error)
            
            if isinstance(value, Continue):
                error = Error("Semantic", "Instruction Continue out of loop", instruction.row, instruction.column)
                tree.get_errors().append(error)
                tree.get_update(error)

            if isinstance(value, Return):
                if tree.get_debugg():
                    tree.get_input_text().tag_remove("debugg", f"{instruction.row}.0", f"{instruction.row + 1}.0")
                    tree.get_input_text().tag_add("debugg", f"{instruction.row}.0", f"{instruction.row + 1}.0")
                    tree.get_input_text().see(f"{instruction.row}.0")
                    var = msg.askyesno(title="Debugger", message="Continue?...")
                    tree.get_input_text().tag_remove("debugg", f"{instruction.row}.0", f"{instruction.row + 1}.0")
                    if var:
                        pass
                    else:
                        tree.set_debugg(False)
                self.type = value.get_type()
                return value.get_result()

            if tree.get_debugg():

                tree.get_input_text().tag_add("debugg", f"{instruction.row}.0", f"{instruction.row + 1}.0")
                tree.get_input_text().see(f"{instruction.row}.0")
                tree.get_table().delete(*tree.get_table().get_children())
                if isinstance(instruction, Print):
                    tree.get_output_text().delete("1.0", "end")
                    tree.get_output_text().insert('insert', tree.get_console())
                    tree.get_output_text().see('end')
                count = 0
                for variable in new_table.get_variables():
                    if variable.get_type() == type.ARRAY:
                        tree.get_table().insert('', "end", text=variable.get_id(), values=(variable.get_type().name, variable.get_value().get_type().name, variable.get_environment(), variable.get_value(), variable.get_row(), variable.get_column()))
                    else:
                        tree.get_table().insert('', "end", text=variable.get_id(), values=("VARIABLE", variable.get_type().name, variable.get_environment(), variable.get_value(), variable.get_row(), variable.get_column()))
                if isinstance(instruction, Assignment):
                    while count < len(tree.get_table().get_children()) - 1:
                        date = tree.get_table().item(tree.get_table().get_children()[count])
                        if date['text'] == instruction.get_id():
                            break
                        count += 1
                if isinstance(instruction, Declaration):
                    count = -1
                if len(tree.get_table().get_children()) != 0:
                    tree.get_table().see(tree.get_table().get_children()[count])
                var = msg.askyesno(title="Debugger", message="Continue?...")
                tree.get_input_text().tag_remove("debugg", f"{instruction.row}.0", f"{instruction.row + 1}.0")
                if var:
                    continue
                else:
                    tree.set_debugg(False)
        
        return None


    def get_node(self):
        node = Ast_Node("Function")
        node.add_child(self.name)
        node.add_child("(")

        params = Ast_Node("Parameters")
        for parameter in self.params:
            param = Ast_Node("Parameter")
            param.add_child(parameter['type'].name)
            param.add_child(parameter['name'])
            params.add_childs_node(param)
        node.add_childs_node(params)
        node.add_child(")")
        node.add_child("{")

        instructions = Ast_Node("Instructions")
        for inst in self.instructions:
            instructions.add_childs_node(inst.get_node())
        
        node.add_childs_node(instructions)
        node.add_child("}")

        return node

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name

    def get_params(self):
        return self.params
            


