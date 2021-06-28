class Tree:

    def __init__(self, instructions):
        self.__instructions = instructions
        self.__functions = []
        self.__errors = []
        self.__console = ""
        self.__global_table = None
        self.__output_text = None


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

    def set_output_text(self, output):
        self.__output_text = output

    def get_output_text(self):
        return self.__output_text

    