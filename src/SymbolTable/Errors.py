class Error:

    def __init__(self, type, description, row, column):
        self.__type = type
        self.__description = description
        self.__row = row
        self.__column = column

    
    def __str__(self):
        return f"{self.__type} - {self.__description} in [{self.__row}, {self.__column}]"