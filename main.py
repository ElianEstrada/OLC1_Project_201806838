from tkinter import Image, PhotoImage, Tk, Menu, messagebox, filedialog, ttk, Label, Text, scrolledtext, INSERT, CENTER, SE, NW, END, Button, Scrollbar, RIGHT, Y, Frame, Canvas, HORIZONTAL, VERTICAL, simpledialog, WORD
from tkinter.constants import FLAT, GROOVE, RAISED, SEL_FIRST, SEL_LAST, SUNKEN

import os
import subprocess
import re

from grammar import parser, get_errors

#########------------Dictonary for paint words------------#########

reserved_words = [
    'new',
    'if',
    'else',
    'switch',
    'case',
    'print',
    'break',
    'default',
    'while',
    'for',
    'continue',
    'return',
    'read',
    'tolower',
    'toupper',
    'length',
    'truncate',
    'round',
    'typeof',
    'main',
    'true',
    'false',
    'var',
    'null', 
    'int',
    'double',
    'string',
    'char', 
    'boolean'
]


#########------------Functions for GUI---------------##########

fileInput = ""
rowCount = 1
columnCount = 1
string = ""
pathFileJs = ""
errors = []
count_error = len(errors)

###---------New document function---------###
def new(): 
    global fileInput
    fileInput = ""
    txtInput.delete(1.0, END)
    txtOutput.delete(1.0, END)
    positionPush()
    lines()


###---------Open File function---------###
def openFile(e = None): 
    global fileInput
    global errors
    errors = []
    fileInput = filedialog.askopenfile(title = "Open File", filetypes = [("JPR files", "*.jpr")])

    fileText = open(fileInput.name)
    text = fileText.read()

    txtInput.delete(1.0, END)

    for item in paint_words(text):
        txtInput.insert(INSERT, item[1], item[0])
    positionPush()
    fileText.close()
    txtOutput.delete("1.0", "end")
    lbl_error_count.config(text = len(errors))
    lines()


###---------Exit Applicatoin function---------###
def exit():
    value = messagebox.askokcancel("Exit", "Are you sure you want to go out?")
    if value: 
        root.destroy()


###---------Save as function---------###
def save_as(e = None): 
    global fileInput

    text = txtInput.get("1.0", "end")
    txtInput.delete("1.0", "end")
    for item in paint_words(text[0:len(text)-1]):
        txtInput.insert(INSERT, item[1], item[0])

    save_file = filedialog.asksaveasfile(title = "Save File", filetypes = [("JPR files", "*.jpr")], defaultextension = '.jpr')
    with open(save_file.name, "w+") as fileSave:
        fileSave.write(txtInput.get(1.0, END))
    fileInput = save_file


###---------Save function---------###
def save(e = None):
    global fileInput

    if fileInput == "": 
        save_as()
    else: 
        text = txtInput.get("1.0", "end")
        txtInput.delete("1.0", "end")
        for item in paint_words(text[0:len(text)-1]):
            txtInput.insert(INSERT, item[1], item[0])

        with open(fileInput.name, "w") as fileSave: 
            fileSave.write(txtInput.get(1.0, END))



###---------Save function---------###
def paint_writing(*args):

    index = txtInput.index(INSERT)
    text = txtInput.get("1.0", "end")
    txtInput.delete("1.0", "end")

    for item in paint_words(text[0:len(text)-1]):
        txtInput.insert(INSERT, item[1], item[0])

    txtInput.mark_set(INSERT, index)
    txtInput.see(INSERT)



##Imports for Interpreter
from src.SymbolTable.Tree import Tree
from src.SymbolTable.SymbolTable import SymbolTable
from src.Instructions.Main import Main
from src.Instructions.Assignment import Assignment
from src.Instructions.Declaration import Declaration
from src.SymbolTable.Errors import Error
from src.Instructions.Break import Break


###---------Analize function---------###
def analize(e = None): 
    global fileInput
    global string
    global pathFileJs
    global errors

    errors = []
    txtOutput.delete("1.0", "end")

    text = txtInput.get("1.0", "end")
    txtInput.delete("1.0", "end")
    for item in paint_words(text[0:len(text)-1]):
        txtInput.insert(INSERT, item[1], item[0])

    instructions = parser(txtInput.get('1.0', 'end'))
    if instructions == None:
        value = messagebox.showerror("Instructions", "No Instructions for interpret")
        return
    #print(instructions)
    ast = Tree(instructions)
    ts_global = SymbolTable()
    ast.set_global_table(ts_global)

    for error in get_errors():
        ast.get_errors().append(error)
        ast.update_console(error)


    ##-----------First Run for declarations and assignment-----------##
    for instruction in ast.get_instructions():
        if isinstance(instruction, (Declaration, Assignment)):
            value = instruction.interpret(ast, ts_global)
            if isinstance(value, Error):
                ast.get_errors().append(value)
                ast.update_console(value)
            if isinstance(instruction, Break):
                error = Error("Semantic", "The Instruction BREAK is loop or switch instruction", instruction.row, instruction.column)
                ast.get_errors().append(error)
                ast.update_console(error)

    count = 0
    ##-----------Second Run for count main function-----------##
    for instruction in ast.get_instructions():
        
        if isinstance(instruction, Main):
            count += 1

            if count > 1:
                error = Error("Semantic", "The main method is already defined", instruction.row, instruction.column) 
                ast.get_errors().append(error)
                ast.update_console(error)
                break
    
    if count == 1:
        ##-----------Third Run for main function interpret-----------##
        for instruction in ast.get_instructions():
            if isinstance(instruction, Main):
                value = instruction.interpret(ast, ts_global)
                if isinstance(value, Error):
                    ast.get_errors().append(value)
                    ast.update_console(value)
                if isinstance(instruction, Break):
                    error = Error("Semantic", "The Instruction BREAK is loop or switch instruction", instruction.row, instruction.column)
                    ast.get_errors().append(error)
                    ast.update_console(error)

    ##-----------Fourth Run for instruction out main-----------##
    for instruction in ast.get_instructions():
        if not isinstance(instruction, (Main, Declaration, Assignment)):
            error = Error("Semantic", "Instruction outside the main method", instruction.row, instruction.column)
            ast.get_errors().append(error)
            ast.update_console(error)
 
    txtOutput.insert('1.0', ast.get_console())
    errors = ast.get_errors()
    lbl_error_count.config(text = len(errors))
    print(ast.get_console())


def report_error(e = None):
    lexical = ""
    count_lex = 1
    sintactic = ""
    count_sint = 1
    semantic = ""
    count_sem = 1

    for error in errors:
        if error.get_type() == "Lexical":
            lexical += f"""
                                            <tr>
                                                <td> {count_lex} </td>
                                                <td> {error.get_description()} </td>
                                                <td> {error.get_row()} </td>
                                                <td> {error.get_column()} </td>
                                            </tr>"""
            count_lex += 1
        elif error.get_type() == "Sintactic":
            sintactic += f"""
                                            <tr>
                                                <td> {count_sint} </td>
                                                <td> {error.get_description()} </td>
                                                <td> {error.get_row()} </td>
                                                <td> {error.get_column()} </td>
                                            </tr>"""
            count_sint += 1
        else:
            semantic += f"""
                                            <tr>
                                                <td> {count_sem} </td>
                                                <td> {error.get_description()} </td>
                                                <td> {error.get_row()} </td>
                                                <td> {error.get_column()} </td>
                                            </tr>"""
            count_sem += 1

    content = f"""
            <!DOCTYPE html>
                <html>
                    <head>
                        <title>
                            Bug Report 
                        </title>
                        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
                        <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
                    </head>
                    <body class="container grey darken-4 white-text">
                        <h1> <center> Report Errors </center> </h1>
                        <ul class = "collapsible">
                            <li class = "active">
                                <div class = "collapsible-header grey darken-2"> Lexical Errors </div>
                                <div class="collapsible-body">
                                    <table class ="striped">
                                        <thead>
                                            <tr>
                                                <th> No. </th>
                                                <th> Description </th>
                                                <th> Line </th>
                                                <th> Column </th>
                                            </tr>
                                        </thead>
                                        <tbody>{lexical}
                                        </tbody>
                                    </table>
                                </div>
                            </li>
                            <li class = "active">
                                <div class = "collapsible-header grey darken-2"> Sintactic Errors </div>
                                <div class="collapsible-body">
                                    <table class ="striped">
                                        <thead>
                                            <tr>
                                                <th> No. </th>
                                                <th> Description </th>
                                                <th> Line </th>
                                                <th> Column </th>
                                            </tr>
                                        </thead>
                                        <tbody>{sintactic}
                                        </tbody>
                                    </table>
                                </div>
                            </li>
                            <li class = "active">
                                <div class = "collapsible-header grey darken-2"> Semantic Errors </div>
                                <div class="collapsible-body">
                                    <table class ="striped">
                                        <thead>
                                            <tr>
                                                <th> No. </th>
                                                <th> Description </th>
                                                <th> Line </th>
                                                <th> Column </th>
                                            </tr>
                                        </thead>
                                        <tbody>{semantic}
                                        </tbody>
                                    </table>
                                </div>
                            </li>
                        </ul>
                        <script>
                            M.AutoInit();
                        </script>
                    </body>
            </html>"""

    #print(content)

    os.makedirs('report', exist_ok=True)

    with open("report/errors.html", "w+") as fileSave: 
            fileSave.write(content)

    if os.name == 'nt':
        dir_name = os.path.dirname(__file__)
        os.startfile(dir_name + '\\report\\errors.html')
    else: 
        dir_name = os.path.dirname(__file__)
        subprocess.call(["xdg-open", "report/errors.html"])


def paint_words(text):
    text += ' '
    list = []
    value = ''
    c = ''
    flag = False
    count = 0

    while count < len(text):
        c = text[count]
        
        if re.search(r"[a-zA-Z0-9_\.]", c):
            value += c
        elif c == '"':
            if re.match(r'[a-zA-Z][a-zA-Z0-9_]*', value):
                id = []
                id.append("variable")
                id.append(value)
                list.append(id)
                value = ''
            elif re.match(r'(\d+\.\d+|\d+)', value):
                num = []
                num.append("number")
                num.append(value)
                list.append(num)
                value = ''
            value += c
            count += 1
            while count < len(text):
                c = text[count]

                if c == '\n':
                    if re.match(r'\"(\\"|.)*?\"', value):
                        str_in = []
                        str_in.append("string")
                        str_in.append(value)
                        list.append(str_in)
                        #value = ''
                    else:
                        flag = True
                    break 

                value += c

                if c == '\\':
                    value += text[count + 1]
                    count += 2
                    continue


                if c == '"':
                    if re.match(r'\"(\\\'|\\"|[^\'])*?\"', value):
                        str_in = []
                        str_in.append("string")
                        str_in.append(value)
                        list.append(str_in)
                        value = ''
                    else:
                        flag = True
                    break

                count += 1

        elif c == "'":
            if re.match(r'[a-zA-Z][a-zA-Z0-9_]*', value):
                id = []
                id.append("variable")
                id.append(value)
                list.append(id)
                value = ''
            elif re.match(r'(\d+\.\d+|\d+)', value):
                num = []
                num.append("number")
                num.append(value)
                list.append(num)
                value = ''
            value += c
            count += 1
            while count < len(text):
                c = text[count]
                value += c

                if c == '\\':
                    value += text[count + 1]
                    count += 2
                    continue

                if c == '\'' or c == '\n':
                    if re.match(r'\'(\\\'|\\"|\\t|\\n|\\\\|[^\'\\])?\'', value):
                        str_in = []
                        str_in.append("string")
                        str_in.append(value)
                        list.append(str_in)
                        value = ''
                    else:
                        flag = True
                    break

                count += 1

        elif c == '#':
            if re.match(r'[a-zA-Z][a-zA-Z0-9_]*', value):
                id = []
                id.append("variable")
                id.append(value)
                list.append(id)
                value = ''
            elif re.match(r'(\d+\.\d+|\d+)', value):
                num = []
                num.append("number")
                num.append(value)
                list.append(num)
                value = ''
            value += c
            count += 1

            c = text[count]

            if c == '*':
                value += c
                count += 1
                while count < len(text):
                    c = text[count]
                    value += c

                    if c == '*':
                        if text[count + 1] == '#':

                            count += 1
                            c = text[count]
                            count +=1
                            value += c
                            if re.match(r'\#\*(.|\n)*?\*\#', value):
                                com_mult = []
                                com_mult.append("comment")
                                com_mult.append(value)
                                list.append(com_mult)
                                value = ''
                            break
                    count += 1
                continue
            while count < len(text):
                c = text[count]
                value += c
                if c == '\n':
                    if re.match(r'\#.*\n', value):
                        com_mult = []
                        com_mult.append("comment")
                        com_mult.append(value)
                        list.append(com_mult)
                        value = ''
                    break
                
                count += 1
        
        else: 
            if re.match(r'[a-zA-Z][a-zA-Z0-9_]*', value):
                id = []
                id.append("variable")
                id.append(value)
                list.append(id)
                value = ''
            elif re.match(r'(\d+\.\d+|\d+)', value):
                num = []
                num.append("number")
                num.append(value)
                list.append(num)
                value = ''
                
            other = []
            other.append("other")
            other.append(text[count])
            list.append(other)
        
        if value != '' and flag:
            err = []
            err.append("error")
            err.append(value)
            list.append(err)
            value = ''
            flag = False

        count += 1

    for item in list:
        if item[1].lower() in reserved_words:
            item[0] = "reserved"

    return list



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

##-------Label Error Img------##
img_error = PhotoImage(file = "./img/errors.png")
img_error.configure(height = 20)
lbl_error = Label(myFrame, image=img_error, bg="#0e8dac")
#lbl_open.config(cursor = "hand1")
lbl_error.grid(row = 0, column = 5, padx = (20, 0))#, pady = 20, padx = 0)
#lbl_open.bind("<Button>", openFile)

##-------Label Error count------##
lbl_error_count = Label(myFrame, bg="#0e8dac", fg="white", text=count_error, font=("Consolas", 12))
lbl_error_count.grid(row = 0, column = 6)


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
lblPlay.config(cursor = "hand1")
lblPlay.grid(row = 3, column = 0, pady = 0, padx = 0)
lblPlay.bind("<Button>", analize)

##-------Button Debugger------##
img_debug = PhotoImage(file = "./img/bug.png")
img_debug.configure(width = 40)
lbl_debug = Label(myFrame3, image=img_debug, bg="#090b1f", width=25)
lbl_debug.config(cursor = "hand1")
lbl_debug.grid(row = 4, column = 0, pady = 20, padx = 0)
#lbl_debug.bind("<Button>", analize)

##-------Button Report------##
img_report = PhotoImage(file = "./img/report_error.png")
img_report.configure(width = 40)
lbl_report = Label(myFrame3, image=img_report, bg="#090b1f", width=30)
lbl_report.config(cursor = "hand1")
lbl_report.grid(row = 5, column = 0, pady = 0, padx = 0)
lbl_report.bind("<Button>", report_error)
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
barMenu = Menu(root, bg="#090B10", border=0, fg="white")

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
txtLine.config(bg="#0f111a", fg="gray", borderwidth=0, highlightbackground="#0F111A")
txtLine.grid(row = 2, column = 0, pady = (24, 0), padx = 0, sticky="nsew")



##-------Text Area for Input--------##
txtInput = Text(myFrame2, wrap = "none", width = 60, height = 30, font = ("Consolas", 12))
txtInput.focus()
txtInput.config(bg="#0F111A", fg="white", insertbackground="white", border=0, tabs=('0.8c'), highlightbackground="#0F111A", borderwidth=0)
txtInput.grid(row = 2, column = 1, sticky="ns", pady = (24, 0), padx= 0)
#txtInput.bind("<Return>", lines)
#txtInput.bind("<BackSpace>", lines)
txtInput.bind("<<Change>>", lines)
txtInput.bind("<Configure>", lines)
txtInput.bind("<Motion>", lines)
txtInput.bind("<KeyRelease>", paint_writing)
txtInput.bind("<Button>", positionPush)
txtInput.bind("<KeyPress>", position)


##-------Configure for paint words--------##
txtInput.tag_config('reserved', foreground='#56cdff')
txtInput.tag_config('variable', foreground='#d8d8ce')
txtInput.tag_config('number', foreground='#6c83fa')
txtInput.tag_config('string', foreground='#ec9a32')
txtInput.tag_config('comment', foreground='#858585')
txtInput.tag_config('other', foreground='#d8d8ce')
txtInput.tag_config('error', foreground='red')


##-------Scroll for Input Vertical--------##
scroll_input = Scrollbar(myFrame2, command=txtInput.yview, bg="#090B10", activebackground="gray")
scroll_input.grid(row = 2, column = 2, sticky="ns", pady = (24, 0))
scroll_input.config(width=12)
txtInput['yscrollcommand'] = scroll_input.set
txtLine['yscrollcommand'] = scroll_input.set


##-------Scroll for Input Horizontal--------##
scroll_input = Scrollbar(myFrame2, command=txtInput.xview, orient="horizontal",bg="#090B10", activebackground="gray")
scroll_input.grid(row = 3, column = 0, columnspan=3, sticky="ew", pady=(0, 24))
scroll_input.config(width=12)
txtInput['xscrollcommand'] = scroll_input.set
txtLine['xscrollcommand'] = scroll_input.set

##-------Text Area for Output--------##
txtOutput = Text(myFrame2, wrap = 'none', width = 60, height = 30, font = ("Consolas", 12))
txtOutput.focus()
txtOutput.config(bg="#090b10", fg="white", insertbackground="white", tabs=('0.8c'), highlightbackground="#090B10")
txtOutput.grid(row = 2, column = 4, sticky="ns", pady = (24, 0))
txtOutput.bind("<Key>", lambda a: "break")


##-------Scroll for Output--------##
scroll_output = Scrollbar(myFrame2, command=txtOutput.yview, bg="#090B10", activebackground="gray")
scroll_output.grid(row = 2, column = 5, sticky="ns", pady = (24, 0))
scroll_output.config(width=12)
txtOutput['yscrollcommand'] = scroll_output.set


##-------Scroll for Input Horizontal--------##
scroll_output = Scrollbar(myFrame2, command=txtOutput.xview, orient="horizontal", bg="#090B10", activebackground="gray")
scroll_output.grid(row = 3, column = 4, columnspan=2, sticky="ew", pady=(0, 24))
scroll_output.config(width=12)
txtOutput['xscrollcommand'] = scroll_output.set

root.config(menu = barMenu)

root.mainloop()
