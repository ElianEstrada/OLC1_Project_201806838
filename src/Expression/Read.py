from src.Abstract.Instruction import Instruction
from src.SymbolTable.Errors import Error
from src.SymbolTable.Type import type

import tkinter as tk
from tkinter import simpledialog


class Read(Instruction):

    def __init__(self, row, column):
        self.__type = type.STRING
        self.row = row
        self.column = column


    def interpret(self, tree, table):

        tree.get_output_text().insert('insert', tree.get_console())
        #tree.set_console("")

        answer = simpledialog.askstring("Input", "Ingrese un valor", parent=tree.get_output_text())
        tree.get_output_text().delete('1.0', 'end')

        print(answer)

        return answer

    def get_type(self):
        return self.__type