from tkinter import Image, PhotoImage, Tk, Menu, messagebox, filedialog, ttk, Label, Text, scrolledtext, INSERT, CENTER, SE, NW, END, Button, Scrollbar, RIGHT, Y, Frame, Canvas, HORIZONTAL, VERTICAL, simpledialog, WORD
from tkinter.constants import FLAT, GROOVE, RAISED, SEL_FIRST, SEL_LAST, SUNKEN

import os

from grammar import analize_lex

#########------------Functions for GUI---------------##########

fileInput = ""
rowCount = 1
columnCount = 1
string = ""
pathFileJs = ""

###---------New document function---------###
def new(): 
    txtInput.delete(1.0, END)
    positionPush()
    lines()


###---------Open File function---------###
def openFile(e = None): 
    global fileInput
    fileInput = filedialog.askopenfile(title = "Abrir Archivo")

    fileText = open(fileInput.name)
    text = fileText.read()

    txtInput.delete(1.0, END)
    txtInput.insert(INSERT, text)
    positionPush()
    fileText.close()
    lines()


###---------Exit Applicatoin function---------###
def exit():
    value = messagebox.askokcancel("Salir", "Está seguro que desea salir?")
    if value: 
        root.destroy()


###---------Save as function---------###
def save_as(e = None): 
    global fileInput

    save_file = filedialog.asksaveasfile(title = "Guardar Archivo")
    with open(save_file.name, "w+") as fileSave:
        fileSave.write(txtInput.get(1.0, END))
    fileInput = save_file.name


###---------Save function---------###
def save(e = None):
    global fileInput

    if fileInput == "": 
        save_as()
    else: 
        with open(fileInput.name, "w") as fileSave: 
            fileSave.write(txtInput.get(1.0, END))


###---------Analize function---------###
def analize(e = None): 
    global fileInput
    global string
    global pathFileJs

    analize_lex(txtInput.get("1.0", "end"))




###---------Current row function---------###
def current_row(flag, flag2 = False): 
    global rowCount
    global columnCount

    end = int(txtInput.index("end").split('.')[0]) - 1

    if rowCount < end:
        flag2 = True

    if flag and flag2: 
        rowCount += 1
        lblRow2.config(text = rowCount)
    elif rowCount != 1 and columnCount == 1 and not flag: 
        rowCount -= 1
        lblRow2.config(text = rowCount)
    elif rowCount != 1 and flag2 and not flag:
        rowCount -= 1
        lblRow2.config(text = rowCount)


###---------Current Column function---------###
def current_column(flag): 
    global columnCount
    if flag: 
        columnCount += 1
        lblColumn2.config(text = columnCount)
    elif columnCount != 1: 
        columnCount -= 1
        lblColumn2.config(text = columnCount)

###---------Position function---------###
#current position before keyrelease
def position(e): 
    global columnCount
    if e.keysym == "Up": 
        current_row(False, True)
    elif e.keysym == "Down": 
        current_row(True)
    elif e.keysym == "Left": 
        current_column(False)
    elif e.keysym == "Right": 
        current_column(True)
    elif e.keysym == "Return": 
        current_row(True, True)
        columnCount = 0
        current_column(True)
    elif e.keysym == "BackSpace":
        current_row(False)
        current_column(False)
    else:
        current_column(True)

###---------Position Push function---------###
#current position before click of editor
def positionPush(e = None): 
    global rowCount
    global columnCount
    #messagebox.showinfo("hola", e.keysym)
    positions = txtInput.index("current").split('.')
    lblRow2.config(text = positions[0])
    rowCount = int(positions[0])
    column = int(positions[1]) + 1
    columnCount = column
    lblColumn2.config(text = column)


###--------------lines function-----------------###
def lines(*args):
    txtLine.delete("1.0", END)
    cont = txtInput.index("@1,0")
    while True:
        dline = txtInput.dlineinfo(cont)
        if dline is None:
            break
        y = dline[1]
        strline = str(cont).split('.')[0]
        #txtLine.inse
        #print(y, strline)
        txtLine.insert(cont, strline + '\n')
        cont = txtInput.index(f"{cont}+1line")

###---------Reports function---------###
def cssReport(): 
    txtOutput.delete(1.0, END)
    txtOutput.insert(INSERT, string)


#########------------GUI---------------##########

##-------root of windows------##
root = Tk()
root.title("LABORATORIO")

##-------Bottom Frame------##
myFrame = Frame()
myFrame.pack(side = "bottom", fill = "x")
myFrame.config(bg = "#0e8dac", width = "920", height = "20")

##-------Label for row------##
lblRow = Label(myFrame, text = "Row: ", fg = "white", bg = "#0e8dac", font=("Consolas", 12))
lblRow.grid(row = 0, column = 0)

lblRow2 = Label(myFrame, text= rowCount, fg="white", bg= "#0e8dac", font=("Consolas", 12))
lblRow2.grid(row = 0, column = 1)

##-------Label for column------##
lblColumn = Label(myFrame, text = "Column: ", fg = "white", bg = "#0e8dac", font=("Consolas", 12))
lblColumn.grid(row = 0, column = 3)

lblColumn2 = Label(myFrame, text= columnCount, fg="white", bg= "#0e8dac", font=("Consolas", 12))
lblColumn2.grid(row = 0, column = 4)


##-------Left Frame for functions------##
myFrame3 = Frame()
myFrame3.pack(side = "left", fill = "y")
myFrame3.config(bg = "#090b1f", width = "50", height = "550", padx=20)

##-------Button New File------##
img_code = PhotoImage(file = "./img/code.png")
img_code.configure(width = 40)
lbl_open = Label(myFrame3, image=img_code, bg="#090b1f", width=25)
lbl_open.config(cursor = "hand1")
lbl_open.grid(row = 0, column = 0, pady = 20, padx = 0)
lbl_open.bind("<Button>", openFile)

##-------Button Save File------##
img_save = PhotoImage(file = "./img/save.png")
img_save.configure(width = 40)
lbl_save = Label(myFrame3, image=img_save, bg="#090b1f", width=30)
lbl_save.config(cursor = "hand1")
lbl_save.grid(row = 1, column = 0, pady = 0, padx = 0)
lbl_save.bind("<Button>", save)

##-------Button Save File as------##
img_save_as = PhotoImage(file = "./img/save-as.png")
img_save_as.configure(width = 40)
lbl_save_as = Label(myFrame3, image=img_save_as, bg="#090b1f", width=30)
lbl_save_as.config(cursor = "hand1")
lbl_save_as.grid(row = 2, column = 0, pady = 20, padx = 0)
lbl_save_as.bind("<Button>", save_as)

##-------Button Play------##
img_play = PhotoImage(file = "./img/play.png")
img_play.configure(width = 40)
lblPlay = Label(myFrame3, image=img_play, bg="#090b1f", width=25)
lblPlay.config(cursor = "hand1", )
lblPlay.grid(row = 3, column = 0, pady = 0, padx = 0)
lblPlay.bind("<Button>", analize)

##-------Button Debugger------##
img_debug = PhotoImage(file = "./img/bug.png")
img_debug.configure(width = 40)
lbl_debug = Label(myFrame3, image=img_debug, bg="#090b1f", width=25)
lbl_debug.config(cursor = "hand1", )
lbl_debug.grid(row = 4, column = 0, pady = 20, padx = 0)
#lbl_debug.bind("<Button>", analize)


##-------Frame for Space left------##
myFrame4 = Frame()
myFrame4.pack(side = "left", fill = "y")
myFrame4.config(bg = "#090b10", width = "20", height = "550", padx=20)

##-------Frame for Space right------##
myFrame5 = Frame()
myFrame5.pack(side = "right", fill = "y")
myFrame5.config(bg = "#090b10", width = "20", height = "550", padx=20)

##-------Main Frame------##
myFrame2 = Frame()
myFrame2.pack(fill = "both", expand = "yes")
myFrame2.config(bg = "#090B10", width = "920", height = "550")

##-------Label for Title------##
lblTitle = Label(myFrame2, text = "ML WEB EDITOR", fg = "white", bg = "#090B10")
lblTitle.config(font = ("Consolas", 28))
lblTitle.grid(row = 0, columnspan=6)
#lblTitle.pack(anchor = CENTER)

lblSpace = Label(myFrame2)
lblSpace.config(width = 5, background="#090b10")
lblSpace.grid(row = 1, column = 3)

##-------Label of Input------##
lblInput = Label(myFrame2, text = "ENTRADA", fg = "white", bg = "#090B10")
lblInput.config(font = ("Consolas", 18))
lblInput.grid(row = 1, column = 1)

##-------Label of Output------##
lblOutput = Label(myFrame2, text = "SALIDA", fg = "white", bg= "#090B10")
lblOutput.config(font = ("Consolas", 18))
lblOutput.grid(row = 1, column = 4)


##-------Bar Menú------##
barMenu = Menu(root, bg="blue")

##-------File Menu------##
fileMenu = Menu(barMenu, tearoff = 0, bg="#090B10", fg="white", activebackground="gray")
fileMenu.config(border=0)
fileMenu.add_command(label = "Nuevo", command = new)
fileMenu.add_command(label = "Abrir", command = openFile)
fileMenu.add_command(label = "Guardar...", command = save)
fileMenu.add_command(label = "Guardar Como...", command= save_as)
fileMenu.add_separator()
fileMenu.add_command(label = "Salir", command = exit)
barMenu.add_cascade(label = "Archivos", menu= fileMenu)

##-------Reports Menu------##
reportMenu = Menu(barMenu, tearoff = 0, bg="#090B10", fg="white", activebackground="gray")
reportMenu.add_command(label = "Reporte de Css", command = cssReport)
barMenu.add_cascade(label =  "Reportes", menu = reportMenu)



##-------Text Area for lines--------##
txtLine = Text(myFrame2, width = 3, height = 30, font = ("Consolas", 12))
txtLine.config(bg="#0f111a", fg="gray", border = 0)
txtLine.grid(row = 2, column = 0, pady = 24, padx = 0, sticky="ew")



##-------Text Area for Input--------##
txtInput = Text(myFrame2, wrap = "word", width = 60, height = 30, font = ("Consolas", 12))
txtInput.focus()
txtInput.config(bg="#0F111A", fg="white", insertbackground="white", border=0)
txtInput.grid(row = 2, column = 1, sticky="ns", pady = 24, padx= 0)
#txtInput.bind("<Return>", lines)
#txtInput.bind("<BackSpace>", lines)
txtInput.bind("<<Change>>", lines)
txtInput.bind("<Configure>", lines)
txtInput.bind("<Motion>", lines)
txtInput.bind("<Button>", positionPush)
txtInput.bind("<KeyPress>", position)


##-------Scroll for Input--------##
scroll_input = Scrollbar(myFrame2, command=txtInput.yview)
scroll_input.grid(row = 2, column = 2, sticky="ns", pady = 24)
scroll_input.config(width=12)
txtInput['yscrollcommand'] = scroll_input.set
txtLine['yscrollcommand'] = scroll_input.set


##-------Text Area for Output--------##
txtOutput = Text(myFrame2, wrap = WORD, width = 60, height = 30, font = ("Consolas", 12))
txtOutput.focus()
txtOutput.config(bg="#090b10", fg="white", insertbackground="white")
txtOutput.grid(row = 2, column = 4, sticky="ns", pady = 24)
txtOutput.bind("<Key>", lambda a: "break")


##-------Scroll for Output--------##
scroll_output = Scrollbar(myFrame2, command=txtInput.yview)
scroll_output.grid(row = 2, column = 5, sticky="ns", pady = 24)
scroll_output.config(width=12)
txtOutput['yscrollcommand'] = scroll_output.set


root.config(menu = barMenu)

root.mainloop()
