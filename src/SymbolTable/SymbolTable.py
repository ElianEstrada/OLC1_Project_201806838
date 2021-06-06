from .Errors import Error

class SymbolTable:

    def __init__(self, prev = None):
        self.__table = {}
        self.__prev = prev
        self.__functions = []



    #Function for setter one variable in table
    def set_table(self, symbol):
        if symbol.get_id() in self.__table:     #Verify if variable exist in table
            return Error("Semantic", f"The variable {symbol.get_id()} already definited", symbol.get_row(), symbol.get_column())
        
        #if not exist add to table
        self.__table[symbol.get_id()] = symbol
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
                self.__table[symbol.get_id()].setValue(symbol.get_value())
                self.__table[symbol.get_id()].setType(symbol.get_type())
                return "Update Variable"
            current_table = current_table.__prev
        return None


