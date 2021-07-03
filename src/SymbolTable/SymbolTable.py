from .Errors import Error
from .Type import type

variables = []

class SymbolTable:

    def __init__(self, prev = None, name = "Global", widget = None):
        self.__name = name
        self.__table = {}
        self.__prev = prev
        self.__widget = widget
        self.__functions = []



    #Function for setter one variable in table
    def set_table(self, symbol):
        if symbol.get_id().lower() in self.__table:     #Verify if variable exist in table
            return Error("Semantic", f"The variable {symbol.get_id()} already definited", symbol.get_row(), symbol.get_column())
        
        # if symbol.get_type() != type.ARRAY:
        #     #self.__widget.delete(*self.__widget.get_children())
           
        #     if self.__widget != None:
        #         self.__widget.insert('', "end", text=symbol.get_id().lower(), values=("Variable", symbol.get_type().name, self.__name, symbol.get_value(), symbol.get_row(), symbol.get_column()))
        # else:
        #     if self.__widget != None:
        #         print(symbol.get_value().get_list_value())
        #         self.__widget.insert('', "end", text=symbol.get_id().lower(), values=(symbol.get_type().name, symbol.get_value().get_type(), self.__name, str(symbol.get_value().get_list_value()), symbol.get_row(), symbol.get_column()))
        flag = True
        for item in variables:
            if item.get_id().lower() == symbol.get_id().lower() and item.get_environment() != self.__name:
                flag = True
            elif item.get_id().lower() == symbol.get_id().lower():
                flag = False

        if flag: 
            variables.append(symbol)

        #if not exist add to table
        symbol.set_environment(self.__name)
        self.__table[symbol.get_id().lower()] = symbol
        return None

    #Function for getter the value of variable
    def get_table(self, id):
        current_table = self

        while(current_table != None):
            if id in current_table.__table:
                return current_table.__table[id]
            current_table = current_table.__prev
        return None

    def update_table(self, symbol):
        current_table = self
        while(current_table != None):
            if symbol.get_id() in current_table.__table:

                if current_table.__table[symbol.get_id()].get_type() == symbol.get_type():    
                    current_table.__table[symbol.get_id()].set_value(symbol.get_value())

                    return None

                elif current_table.__table[symbol.get_id()].get_type() == type.NULL or symbol.get_type() == type.NULL:
                    current_table.__table[symbol.get_id()].set_value(symbol.get_value())
                    current_table.__table[symbol.get_id()].set_type(symbol.get_type())

                    return None

                else:
                    return Error("Semantic", f"Cannot assign value of type: {symbol.get_type().name} in a variable of type: {current_table.__table[symbol.get_id()].get_type().name}", symbol.get_row(), symbol.get_column())

            current_table = current_table.__prev
        return Error("Semantic", f"The id: {symbol.get_id()} doesn't exist in current context", symbol.get_row(), symbol.get_column())


    def get_name(self):
        return self.__name

    def set_widget(self, widget):
        self.__widget = widget

    def get_widget(self):
        return self.__widget

    def get_variables(self):
        global variables
        return variables