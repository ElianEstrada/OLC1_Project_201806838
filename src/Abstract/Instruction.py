from abc import ABC, abstractmethod

class Instruction(ABC):

    def __init__(self, row, column):
        self.row = row
        self.column = column
        super().__init__()

    @abstractmethod
    def interpret(self, tree, table):
        pass