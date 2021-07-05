from src.Abstract.Ast_Node import Ast_Node
from src.Expression.Relational import Relational
from src.Instructions.Break import Break
from src.Instructions.Continue import Continue
from src.Instructions.Return import Return
from src.Instructions.Print import Print
from src.Instructions.Assignment import Assignment
from src.Instructions.Declaration import Declaration
from src.Abstract.Instruction import Instruction
from src.SymbolTable.SymbolTable import SymbolTable
from src.SymbolTable.Errors import Error
from src.SymbolTable.Type import type, Relational_Operators

import tkinter.messagebox as msg

class Switch(Instruction):

    def __init__(self, exp, list_case, default, row, column):
        self.__exp = exp
        self.__list_case = list_case
        self.__default = default
        self.__row_case = 0
        self.__column_case = 0
        self.row = row
        self.column = column
        self.__flag = False

    
    """ def interpret(self, tree, table):

        value_exp = self.__exp.interpret(tree, table)

        if isinstance(value_exp, Error):
            return value_exp

        if self.__exp.get_type() in (type.INTEGGER, type.FLOAT, type.CHAR, type.STRING, type.BOOLEAN):
            
            if self.__list_case != None:

                for item_case in self.__list_case:
                    value_case = item_case.interpret(tree, table)

                    if str(value_case) == str(value_exp):

                        if self.execute_instructions(tree, table, item_case.get_instructions(), True) == None and not self.__flag:
                            return None
                        
                    elif self.__flag:
                        self.__flag = False

                        if self.execute_instructions(tree, table, item_case.get_instructions(), True) == None and not self.__flag:
                            return None

                if self.__default != None:
                    return self.execute_instructions(tree, table, self.__default)
            elif self.__default != None:
                return self.execute_instructions(tree, table, self.__default)

        else:
            return Error("Semantic", f"Expression of type {self.__exp.get_type().name} was not expected", self.row, self.column) """

    def interpret(self, tree, table):

        if self.__list_case != None:

            for item in self.__list_case:

                relation = Relational(self.__exp, item.get_value(), Relational_Operators.EQUAL, self.row, self.column)

                result = relation.interpret(tree, table)

                if isinstance(result, Error):
                    return result
                
                if result == "true":
                    self.__row_case = item.row
                    self.__column_case = item.column
                    result_interpret = self.execute_instructions(tree, table, item.get_instructions(), True)
                    if result_interpret == None and not self.__flag:
                            return None
                    elif isinstance(result_interpret, Return):
                        return result_interpret

                elif self.__flag:
                        self.__flag = False

                        # if self.execute_instructions(tree, table, item.get_instructions(), True) == None and not self.__flag:
                        #     return None

            if self.__default != None:
                    return self.execute_instructions(tree, table, self.__default)
        
        elif self.__default != None:
                return self.execute_instructions(tree, table, self.__default)


    def get_node(self):
        node = Ast_Node("Switch")
        node.add_child("switch")
        node.add_child("(")
        node.add_childs_node(self.__exp.get_node())
        node.add_child(")")
        node.add_child("{")

        if self.__list_case != None:
            cases = Ast_Node("Cases")
            for case in self.__list_case:
                cases.add_childs_node(case.get_node())
            node.add_childs_node(cases)

        if self.__default != None:
            default = Ast_Node("Default")
            default.add_child("default")
            default.add_child(":")
            inst_default = Ast_Node("Instructions")
            for inst in self.__default:
                inst_default.add_childs_node(inst.get_node())
            default.add_childs_node(inst_default)

            node.add_childs_node(default)
        
        node.add_child("}")

        return node


    def execute_instructions(self, tree, table, instructions, flag = False):
        if flag:
            new_table = SymbolTable(table, f"Switch-Case-{self.__row_case}-{self.__column_case}", table.get_widget())
        else:
            new_table = SymbolTable(table, f"Switch-Default-{self.row}-{self.column}", table.get_widget())

        for item in instructions:
            instruction = item.interpret(tree, new_table)

            if isinstance(instruction, Error):
                tree.get_errors().append(instruction) 
                tree.update_console(instruction)
                continue
            
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

        if flag:
            self.__flag = True