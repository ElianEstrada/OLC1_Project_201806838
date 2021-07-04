from src.Abstract.Ast_Node import Ast_Node
from src.Instructions.Continue import Continue
from src.Instructions.Return import Return
from src.Abstract.Instruction import Instruction
from src.SymbolTable.Errors import Error
from src.SymbolTable.Type import type
from src.Instructions.Break import Break
from src.SymbolTable.SymbolTable import SymbolTable


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
                self.type = value.get_type()
                return value.get_result()
        
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
            


