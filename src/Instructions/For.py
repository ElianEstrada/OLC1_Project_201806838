from src.Abstract.Ast_Node import Ast_Node
from src.Instructions.Continue import Continue
from src.SymbolTable.SymbolTable import SymbolTable
from src.Abstract.Instruction import Instruction
from src.Instructions.Break import Break
from src.Instructions.Return import Return
from src.Instructions.Print import Print
from src.Instructions.Assignment import Assignment
from src.Instructions.Declaration import Declaration
from src.SymbolTable.Type import type
from src.SymbolTable.Errors import Error

import tkinter.messagebox as msg

class For(Instruction):

    def __init__(self, init, condition, advance, instructions, row, column):
        self.__init = init
        self.__condition = condition
        self.__advance = advance
        self.__instructions = instructions
        self.__count = 0
        self.row = row
        self.column = column

    
    def interpret(self, tree, table):


        if None not in (self.__init, self.__condition, self.__advance):
            new_table = None
            declar_flag = False
            if isinstance(self.__init, Declaration):
                new_table = SymbolTable(table, f"Init_For-{self.__init.row}-{self.__init.column}", table.get_widget())
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
                            if self.__count == 0:
                                new_table = SymbolTable(table, f"For-{self.row}-{self.column}", table.get_widget())
                            else:
                                new_table = SymbolTable(table, f"For-{self.row}-{self.column}")
                        else:
                            if self.__count == 0:
                                new_table = SymbolTable(new_table, f"For-{self.row}-{self.column}", new_table.get_widget())
                            else:
                                new_table = SymbolTable(new_table, f"For-{self.row}-{self.column}")

                        if self.__instructions != None:
                            for item in self.__instructions:
                                instruction = item.interpret(tree, new_table)

                                if isinstance(instruction, Error):
                                    tree.get_errors().append(instruction)
                                    tree.update_console(instruction)
                                
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
                                    break

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
                                    return None
                                
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
                                        continue
                                    else:
                                        tree.set_debugg(False)

                        advance = self.__advance.interpret(tree, new_table)
                        
                        if isinstance(advance, Error):
                            return advance
                    else:
                        break
                else:
                    return Error("Semantic", f"Expect a Boolean type expression not of type {self.__exp.get_typ().name}", self.row, self.column)
                
                self.__count += 1

        else:
            return Error("Semantic", "Expression Expected", self.row, self.column)

    def get_node(self):
        node = Ast_Node("For")
        node.add_child("for")
        node.add_child("(")
        node.add_childs_node(self.__init.get_node())
        
        node.add_child(";")
        node.add_childs_node(self.__condition.get_node())
        node.add_child(";")
        node.add_childs_node(self.__advance.get_node())
        node.add_child(";")
        node.add_child(")")
        node.add_child("{")

        instructions = Ast_Node("Instructions")

        for inst in self.__instructions:
            instructions.add_childs_node(inst.get_node())

        node.add_childs_node(instructions)

        node.add_child("}")


        return node