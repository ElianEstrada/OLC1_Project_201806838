from src.Abstract.Instruction import Instruction

class Primitive(Instruction):

    def __init__(self, type, value, row, column):
        self.__type = type
        self.__value = value
        self.row = row
        self.column = column

    def interpret(self, tree, table):
        return self.__value

    def set_type(self, type):
        self.__type = type
    
    def get_type(self):
        return self.__type

    def set_value(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

    def __str__(self):
        return f"{self.__type} - {self.__value} in [{self.row}, {self.column}]"

        