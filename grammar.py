reserved_words = {

    "new": "res_new", 
    "if": "res_if",
    "else": "res_else",
    "switch": "res_switch",
    "case": "res_case",
    "print": "res_print", 
    "break": "res_break",
    "default": "res_default",
    "while": "res_while",
    "for": "res_for",
    "continue": "res_continue",
    "return": "res_return",
    "read": "res_read",
    "tolower": "res_tolower",
    "toupper": "res_toupper",
    "length": "res_length",
    "truncate": "res_truncate",
    "round": "res_round",
    "typeof": "res_typeof",
    "main": "res_main", 
    "true": "res_true",
    "false": "res_false", 
    "var": "res_var"

}

tokens = [

    "tk_key_o",
    "tk_key_c",
    "tk_par_o",
    "tk_par_c",
    "tk_brackets_o",
    "tk_brackets_c",
    "tk_dotcomma",
    "tk_comma",
    "tk_twodot",
    "tk_inc",
    "tk_dec",
    "tk_add",
    "tk_sub",
    "tk_mult",
    "tk_div",
    "tk_pow",
    "tk_module",
    "tk_equals",
    "tk_assig",
    "tk_different",
    "tk_greater_equals",
    "tk_greater",
    "tk_less_equals",
    "tk_less",
    "tk_or",
    "tk_and",
    "tk_not",
    "tk_decimal",
    "tk_int",
    "tk_string",
    "tk_char",
    "tk_id"
    

] + list(reserved_words.values())

#Tokens definition

t_tk_key_o              = r'{'
t_tk_key_c              = r'}'
t_tk_par_o              = r'\('
t_tk_par_c              = r'\)'
t_tk_brackets_o         = r'\['
t_tk_brackets_c         = r'\]'
t_tk_dotcomma           = r';'
t_tk_comma              = r','
t_tk_twodot             = r':'
t_tk_inc                = r'\+\+'
t_tk_dec                = r'--'
t_tk_pow                = r'\*\*'
t_tk_add                = r'\+'
t_tk_sub                = r'-'
t_tk_mult               = r'\*'
t_tk_div                = r'/'
t_tk_module             = r'\%'
t_tk_equals             = r'=='
t_tk_different          = r'=!'
t_tk_assig              = r'='
t_tk_greater_equals     = r'>='
t_tk_greater            = r'>'
t_tk_less_equals        = r'<='
t_tk_less               = r'<'
t_tk_or                 = r'\|\|'
t_tk_and                = r'&&'
t_tk_not                = r'!'


def t_tk_decimal(t):
    r'\d+\.\d+'

    try:
        t.value = float(t.value)
    except ValueError:
        print(f"Float value too large {t.value}")
        t.value = 0
    return t

def t_tk_int(t):
    r'\d+'
    
    try:
        t.value = int(t.value)
    except ValueError:
        print(f"Int value too large {t.value}")
        t.value = 0
    return t

def t_tk_id(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved_words.get(t.value.lower(), "tk_id")
    return t

def t_tk_string(t):
    r'\".*\"'
    t.value = t.value[1:-1]

    t.value = t.value.replace('\\t', '\t')
    t.value = t.value.replace('\\n', '\n')
    t.value = t.value.replace('\\"', '\"')
    t.value = t.value.replace("\\'", "\'")
    t.value = t.value.replace('\\\\', '\\')

    return t

def t_tk_char(t):
    #r'\'\\?.\''
    r'\'(\\\'|\\"|\\t|\\n|\\\\|.)\''
    
    t.value = t.value[1:-1]
    print(t.value)
    t.value = t.value.replace('\\t', '\t')
    t.value = t.value.replace('\\n', '\n')
    t.value = t.value.replace('\\"', '\"')
    t.value = t.value.replace("\\'", "\'")
    t.value = t.value.replace('\\\\', '\\')

    return t

##multipleline comment

def t_multipleline_comment(t):
    r'\#\*(.|\n)*?\*\#'
    t.lexer.lineno += t.value.count('\n')

##simple comment

def t_simple_comment(t):
    r'\#.*\n'
    t.lexer.lineno += 1


#Ignorated chararcter
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


def find_column(input_token, token):
    line_start = input_token.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

from tkinter.constants import NONE
import ply.lex as lex
lexer = lex.lex()


errors = []

#Precedence and Asosiation
precedence = (
    ('left', 'tk_add', 'tk_sub'),
    ('left', 'tk_mult', 'tk_div'),
)

#Grammar Definition

#Abstract
from src.Abstract.Instruction import Instruction
from src.Instructions.Print import Print
from src.Expression.Primitive import Primitive
from src.Expression.Arithmetic import Arithmetic
from src.SymbolTable.Type import type, Arithmetic_Operator
from src.SymbolTable.Errors import Error


start = 'init'

###---------Production Init---------###
def p_init(t):
    'init : instructions'
    t[0] = t[1]

###---------Production instructions---------###

def p_instructions(t):
    'instructions : instructions instruction'
    if t[2] != None:
        t[1].append(t[2])
    t[0] = t[1]

def p_instructions_instruction(t):
    'instructions : instruction'
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [t[1]]

###---------Production instruction---------###

def p_instruction(t):
    '''instruction : statement ptcommaP
                   | assignment ptcommaP 
                   | print ptcommaP
                   | functions'''
    t[0] = t[1]

def p_instruction_error(t):
    'instruction : error tk_dotcomma'
    print(f"Error sintáctico: {str(t[1].value)}, {t.lineno(1)}, {find_column(input, t.slice[1])}")
    #errors.append(f"Error sintáctico: {str(t[1].value)}, {t.lineno(1)}, {find_column(input, t.slice[1])}")
    errors.append(Error("Sintactic", f"Sintactic error {str(t[1].value)}", t.lineno(1), find_column(input, t.slice[1])))
    t[0] = None

###---------Production Statement---------###

def p_statement(t):
    'statement : res_var tk_id statementP'
    if t[3] != None:
        t[0] = t[1] + t[2] + t[3]
    else:
        t[0]  = t[1] + t[2]


def p_statementP(t):
    '''statementP : tk_assig expression
                  | empty'''
    if t[1] != None:
        t[0] = t[1] + str(t[2])
    else:
        t[0] = t[1]

###---------Production Assignment---------###

def p_assignment(t):
    'assignment : tk_id tk_assig expression'
    t[0] = t[1] + t[2] + str(t[3])


###---------Production Functions---------###

def p_functions(t):
    'functions : function_main'
    t[0] = t[1]

###---------Production function_main---------###

def p_function_main(t):
    'function_main : res_main tk_par_o tk_par_c tk_key_o instructions tk_key_c'
    t[0] = t[1] + t[2] + t[3] + t[4] + str(t[5]) + t[6]


###---------Production print---------###

def p_print(t):
    'print : res_print tk_par_o expression tk_par_c'
    t[0] = Print(t[3], t.lineno(1), find_column(input, t.slice[1]))

###---------Production ptcommaP---------###

def p_ptcommaP(t):
    '''ptcommaP : tk_dotcomma
                | empty'''
    t[0] = t[1]


###---------Production Expression---------###

def p_expression_binary(t):
    '''expression : expression tk_add expression
                  | expression tk_sub expression'''
    
    if t[2] == '+':
        t[0] = Arithmetic(t[1], t[3], Arithmetic_Operator.ADDITION, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-':
        t[0] = Arithmetic(t[1], t[3], Arithmetic_Operator.SUBSTRACTION, t.lineno(2), find_column(input, t.slice[2]))


def p_expression_primitive(t):
    '''
    expression :  tk_int
    '''
    t[0] = Primitive(type.INTEGGER, t[1], t.lineno(1), find_column(input, t.slice[1]))

###---------Production empty---------###

def p_empty(t):
    'empty : '
    pass

import ply.yacc as yacc
parser = yacc.yacc()


input = ''

def getErrors():
    return errors

def parser(str_input):
    global errors
    global input
    errors = []
    lexer = lex.lex()
    parser = yacc.yacc()

    input = str_input
    return parser.parse(str_input)