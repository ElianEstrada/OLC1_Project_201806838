class Tree:

    def __init__(self, instructions):
        self.__instructions = instructions
        self.__functions = []
        self.__errors = []
        self.__console = ""
        self.__symbol_table = []
        self.__global_table = None
        self.__output_text = None
        self.__debugg = False
        self.__table = None
        self.__dot = ""
        self.__count = 0


    def set_instructions(self, instructions):
        self.__instructions = instructions
    
    def get_instructions(self):
        return self.__instructions

    def add_function(self, function):
        self.__functions.append(function)
    
    def get_function(self, name):

        for item in self.__functions:
            if item.get_name() == name:
                return item
        
        return None

    def get_function_all(self):
        return self.__functions

    def set_errors(self, errors):
        self.__errors = errors
    
    def get_errors(self):
        return self.__errors
    
    def set_console(self, console):
        self.__console = console
    
    def get_console(self):
        return self.__console

    def update_console(self, input):
        self.__console += str(input) + '\n'
    
    def set_global_table(self, global_table):
        self.__global_table = global_table
    
    def get_global_table(self):
        return self.__global_table
    
    def set_symbol_table(self, symbol_table):
        self.__symbol_table = symbol_table

    def get_symbol_table(self):
        return self.__symbol_table

    def set_output_text(self, output):
        self.__output_text = output

    def get_output_text(self):
        return self.__output_text

    def set_table(self, table):
        self.__table = table

    def get_table(self):
        return self.__table

    def set_debugg(self, debugg):
        self.__debugg = debugg
    
    def get_debugg(self):
        return self.__debugg

    def get_dot(self, root):
        self.__dot = ""
        self.__dot += 'digraph {\nranksep="2";\nbgcolor = "#090B10";\nedge[color="#56cdff"];\nnode [style="filled" fillcolor = "#0F111A" fontcolor = "white" color = "#007acc"];'
        self.__dot += 'n0[label="' + root.get_value().replace("\"", "\\\"") + '"];\n'
        self.__count = 1
        self.travel_ast("n0", root)
        self.__dot += "}"
        return self.__dot


    def travel_ast(self, id_root, node_root):
        for child in node_root.get_childs():
            name_child = f"n{self.__count}"
            self.__dot += name_child + ' [label = "' + child.get_value().replace("\"", "\\\"") + '"];\n'
            self.__dot += f"{id_root} -> {name_child};\n"
            self.__count += 1
            self.travel_ast(name_child, child)

    