class Error:

    def __init__(self, type, description, row, column):
        self.__type = type
        self.__description = description
        self.__row = row
        self.__column = column

    
    def get_type(self):
        return self.__type

    def get_description(self):
        return self.__description

    def get_row(self):
        return self.__row
    
    def get_column(self):
        return self.__column

    def __str__(self):
        return f"--->{self.__type} - {self.__description} in [{self.__row}, {self.__column}]"