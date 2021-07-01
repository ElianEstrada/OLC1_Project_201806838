from src.Abstract.Ast_Node import Ast_Node
from src.Expression.Relational import Relational
from src.Instructions.Break import Break
from src.Instructions.Continue import Continue
from src.Instructions.Return import Return
from src.Abstract.Instruction import Instruction
from src.SymbolTable.SymbolTable import SymbolTable
from src.SymbolTable.Errors import Error
from src.SymbolTable.Type import type, Relational_Operators


class Switch(Instruction):

    def __init__(self, exp, list_case, default, row, column):
        self.__exp = exp
        self.__list_case = list_case
        self.__default = default
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
        node.add_chlid("(")
        node.add_chlids_node(self.__exp.get_node())
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
        
        return node



        node.add_child("}")


    def execute_instructions(self, tree, table, instructions, flag = False):
        new_table = SymbolTable(table)

        for item in instructions:
            instruction = item.interpret(tree, new_table)

            if isinstance(instruction, Error):
                tree.get_errors().append(instruction) 
                tree.update_console(instruction)
            
            if isinstance(instruction, Break):
                return None

            if isinstance(instruction, Continue):
                return instruction

            if isinstance(instruction, Return):
                return instruction

        if flag:
            self.__flag = True