from src.Abstract.Ast_Node import Ast_Node
from src.Instructions.Break import Break
from src.Instructions.Continue import Continue
from src.SymbolTable.SymbolTable import SymbolTable
from src.SymbolTable.Errors import Error
from src.Instructions.Return import Return
from src.Abstract.Instruction import Instruction
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

                    if isinstance(instruction, Continue):
                        return instruction

                    if isinstance(instruction, Break):
                        return instruction

                    if isinstance(instruction, Return):
                        return instruction

                    if tree.get_debugg():
                        var = msg.askyesno(title="Debugger", message="Continue?...")
                        if var:
                            continue
                        else:
                            return
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