class Symbol:

    def __init__(self, id, type, row, column, value):
        self.__id = id.lower()
        self.__type = type
        self.__row = row
        self.__column = column
        self.__value = value


    def set_id(self, id):
        self.__id = id

    def get_id(self):
        return self.__id

    def set_type(self, type):
        self.__type = type

    def get_type(self):
        return self.__type
        
    def set_row(self, row):
        self.__row = row

    def get_row(self):
        return self.__row
    
    def set_column(self, column):
        self.__column = column

    def get_column(self):
        return self.__column

    def set_value(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

    