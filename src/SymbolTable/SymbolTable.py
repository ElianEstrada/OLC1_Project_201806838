from .Errors import Error
from .Type import type

class SymbolTable:

    def __init__(self, prev = None):
        self.__table = {}
        self.__prev = prev
        self.__functions = []



    #Function for setter one variable in table
    def set_table(self, symbol):
        if symbol.get_id().lower() in self.__table:     #Verify if variable exist in table
            return Error("Semantic", f"The variable {symbol.get_id()} already definited", symbol.get_row(), symbol.get_column())
        
        #if not exist add to table
        self.__table[symbol.get_id().lower()] = symbol
        return None

    #Function for getter the value of variable
    def get_table(self, id):
        current_table = self

        while(current_table != None):
            if id in self.__table:
                return self.__table[id]
            current_table = current_table.__prev
        return None

    def update_table(self, symbol):
        current_table = self
        while(current_table != None):
            if symbol.get_id() in self.__table:

                if self.__table[symbol.get_id()].get_type() == symbol.get_type():    
                    self.__table[symbol.get_id()].set_value(symbol.get_value())

                    return None

                elif self.__table[symbol.get_id()].get_type() == type.NULL or symbol.get_type() == type.NULL:
                    self.__table[symbol.get_id()].set_value(symbol.get_value())
                    self.__table[symbol.get_id()].set_type(symbol.get_type())

                    return None

                else:
                    return Error("Semantic", f"Cannot assign value of type: {symbol.get_type()} in a variable of type: {self.__table[symbol.get_id()].get_type()}")

            current_table = current_table.__prev
        return Error("Semantic", f"The id: {symbol.get_id()} doesn't exist in current context", self.row, self.column)


