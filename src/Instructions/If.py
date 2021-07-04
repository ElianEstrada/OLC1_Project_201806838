from src.Instructions.Declaration import Declaration
from src.Abstract.Ast_Node import Ast_Node
from src.Instructions.Break import Break
from src.Instructions.Continue import Continue
from src.SymbolTable.SymbolTable import SymbolTable
from src.SymbolTable.Errors import Error
from src.Instructions.Return import Return
from src.Abstract.Instruction import Instruction
from src.Instructions.Assignment import Assignment
from src.Instructions.Print import Print
from src.SymbolTable.Type import type


import tkinter.messagebox as msg

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

                new_table = SymbolTable(table, f"If-{self.row}-{self.column}", table.get_widget())
             
                for item in self.__instructions:

                    instruction = item.interpret(tree, new_table)

                    if isinstance(instruction, Error):
                        tree.get_errors().append(instruction)
                        tree.update_console(instruction)
                        continue

                    if isinstance(instruction, Continue):
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
                        return instruction

                    if isinstance(instruction, Break):
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
                        return instruction

                    if isinstance(instruction, Return):
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
                        return instruction

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
                            pass
                        else:
                            tree.set_debugg(False)
                    
                    #if debugg
                        #MesseageBox si ok -> continue si no return
            else:
                if self.__else_instructions != None:

                    new_table = SymbolTable(table, f"Else-{self.row}-{self.column}", table.get_widget())
                    for item in self.__else_instructions:

                        instruction_else = item.interpret(tree, new_table)

                        if isinstance(instruction_else, Error):
                            tree.get_errors().append(instruction_else)
                            tree.update_console(instruction_else)
                            continue

                        if isinstance(instruction_else, Continue):
                            if tree.get_debugg():
                                tree.get_input_text().tag_remove("debugg", f"{instruction_else.row}.0", f"{instruction_else.row + 1}.0")
                                tree.get_input_text().tag_add("debugg", f"{instruction_else.row}.0", f"{instruction_else.row + 1}.0")
                                tree.get_input_text().see(f"{instruction_else.row}.0")
                                var = msg.askyesno(title="Debugger", message="Continue?...")
                                tree.get_input_text().tag_remove("debugg", f"{instruction_else.row}.0", f"{instruction_else.row + 1}.0")
                                if var:
                                    pass
                                else:
                                    tree.set_debugg(False)
                            return instruction_else  

                        if isinstance(instruction_else, Break):
                            if tree.get_debugg():
                                tree.get_input_text().tag_remove("debugg", f"{instruction_else.row}.0", f"{instruction_else.row + 1}.0")
                                tree.get_input_text().tag_add("debugg", f"{instruction_else.row}.0", f"{instruction_else.row + 1}.0")
                                tree.get_input_text().see(f"{instruction_else.row}.0")
                                var = msg.askyesno(title="Debugger", message="Continue?...")
                                tree.get_input_text().tag_remove("debugg", f"{instruction_else.row}.0", f"{instruction_else.row + 1}.0")
                                if var:
                                    pass
                                else:
                                    tree.set_debugg(False)
                            return instruction_else

                        if isinstance(instruction_else, Return):
                            if tree.get_debugg():
                                tree.get_input_text().tag_remove("debugg", f"{instruction_else.row}.0", f"{instruction_else.row + 1}.0")
                                tree.get_input_text().tag_add("debugg", f"{instruction_else.row}.0", f"{instruction_else.row + 1}.0")
                                tree.get_input_text().see(f"{instruction_else.row}.0")
                                var = msg.askyesno(title="Debugger", message="Continue?...")
                                tree.get_input_text().tag_remove("debugg", f"{instruction_else.row}.0", f"{instruction_else.row + 1}.0")
                                if var:
                                    pass
                                else:
                                    tree.set_debugg(False)
                            return instruction_else

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

                elif self.__else_if != None:

                    result = self.__else_if.interpret(tree, table)

                    if isinstance(result, Error):
                        return result

                    if isinstance(result, Return):
                        return result

                    if isinstance(result, Break):
                        return result

                    if isinstance(result, Continue):
                        return result

        else: 
            return Error("Semantic", f"Expect a Boolean type expression not of type {self.__exp.get_type().name}", self.row, self.column) 


    def get_node(self):
        node = Ast_Node("If")
        node.add_child("if")
        node.add_child("(")
        node.add_childs_node(self.__exp.get_node())
        node.add_child(")")
        node.add_child("{")

        instructions_if = Ast_Node("If Instructions")
        for inst in self.__instructions:
            instructions_if.add_childs_node(inst.get_node())
        
        node.add_childs_node(instructions_if)
        node.add_child("}")

        if self.__else_instructions != None:
            instructions_else = Ast_Node("Else Instructions")
            node.add_child("else")
            node.add_child("{")
            
            for inst in self.__else_instructions:
                instructions_else.add_childs_node(inst.get_node())

            node.add_childs_node(instructions_else)
            node.add_child("}")

        elif self.__else_if != None:
            node.add_childs_node(self.__else_if.get_node())

        return node