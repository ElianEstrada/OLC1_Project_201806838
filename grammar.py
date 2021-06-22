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
    "var": "res_var", 
    "null": "res_null", 
    "int": "res_int",
    "double": "res_double",
    "char": "res_char",
    "string": "res_string",
    "boolean": "res_boolean"
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
    t.value = t.value.lower()
    return t

def t_tk_string(t):
    r'\"(\\\'|\\"|\\\\|\\n|\\t|[^\'\\\"])*?\"'
    t.value = t.value[1:-1]

    t.value = t.value.replace('\\t', '\t')
    t.value = t.value.replace('\\n', '\n')
    t.value = t.value.replace('\\"', '\"')
    t.value = t.value.replace("\\'", "\'")
    t.value = t.value.replace('\\\\', '\\')

    return t

def t_tk_char(t):
    #r'\'\\?.\''
    r'\'(\\\'|\\"|\\t|\\n|\\\\|[^\'\\\"])?\''
    
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
    errors.append(Error("Lexical", f"This is illegal token {t.value[0]}", t.lexer.lineno, find_column(input, t)))
    t.lexer.skip(1)


def find_column(input_token, token):
    line_start = input_token.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


import ply.lex as lex
lexer = lex.lex()


errors = []

#Precedence and Asosiation
precedence = (
    ('left', 'tk_or'),
    ('left', 'tk_and'),
    ('right', 'tk_unot'),
    ('left', 'tk_equals', 'tk_different', 'tk_greater', 'tk_greater_equals', 'tk_less', 'tk_less_equals'),
    ('left', 'tk_add', 'tk_sub'),
    ('left', 'tk_mult', 'tk_div', 'tk_module'),
    ('left', 'tk_pow'),
    ('right', 'tk_uminus'),
    ('right', 'tk_fcast'),
    ('left', 'tk_inc', 'tk_dec')
)

#Grammar Definition

#Abstract
#from src.Abstract.Instruction import Instruction
from src.Instructions.Print import Print
from src.Expression.Primitive import Primitive
from src.Expression.Identifier import Identifier
from src.Expression.Arithmetic import Arithmetic
from src.Expression.Relational import Relational
from src.Expression.Logic import Logic
from src.Expression.Casting import Casting
from src.SymbolTable.Type import type, Arithmetic_Operator, Relational_Operators, Logical_Operators
from src.Instructions.Main import Main
from src.Instructions.Declaration import Declaration
from src.Instructions.Assignment import Assignment
from src.Instructions.Inc_Dec import Int_Dec
from src.Instructions.If import If
from src.Instructions.Switch import Switch
from src.Instructions.Case import Case
from src.Instructions.While import While
from src.Instructions.For import For
from src.Instructions.Break import Break
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
                   | inc_dec ptcommaP
                   | conditional
                   | loops
                   | transfer ptcommaP
                   | functions'''
    t[0] = t[1]

def p_instruction_error(t):
    'instruction : error tk_dotcomma'
    #print(f"Error sintáctico: {str(t[1].value)}, {t.lineno(1)}, {find_column(input, t.slice[1])}")
    #errors.append(f"Error sintáctico: {str(t[1].value)}, {t.lineno(1)}, {find_column(input, t.slice[1])}")
    errors.append(Error("Sintactic", f"Sintactic error {str(t[1].value)}", t.lineno(1), find_column(input, t.slice[1])))
    t[0] = None

###---------Production Statement---------###

def p_statement(t):
    'statement : res_var tk_id statementP'
    if t[3] != None:
        t[0] = Declaration(t[2], t.lineno(2), find_column(input, t.slice[2]), t[3])
    else:
        t[0]  = Declaration(t[2], t.lineno(2), find_column(input, t.slice[2]))


def p_statementP(t):
    '''statementP : tk_assig expression
                  | empty'''
    if t[1] != None:
        t[0] = t[2]
    else:
        t[0] = t[1]

###---------Production Assignment---------###

def p_assignment(t):
    'assignment : tk_id tk_assig expression'
    t[0] = Assignment(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))


###---------Production Functions---------###

def p_functions(t):
    'functions : function_main'
    t[0] = t[1]

###---------Production function_main---------###

def p_function_main(t):
    'function_main : res_main tk_par_o tk_par_c tk_key_o instructions tk_key_c'
    t[0] = Main(t[5], t.lineno(1), find_column(input, t.slice[1]))


###---------Production print---------###

def p_print(t):
    'print : res_print tk_par_o expression tk_par_c'
    t[0] = Print(t[3], t.lineno(1), find_column(input, t.slice[1]))


###---------Production inc_dec---------###

def p_inc_dec(t):
    '''inc_dec : tk_id tk_inc
               | tk_id tk_dec'''

    if t[2] == '++':
        t[0] = Int_Dec(Identifier(t[1], t.lineno(1), find_column(input, t.slice[1])), Arithmetic_Operator.INC, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '--':
        t[0] = Int_Dec(Identifier(t[1], t.lineno(1), find_column(input, t.slice[1])), Arithmetic_Operator.DEC, t.lineno(2), find_column(input, t.slice[2]))


###---------Production Conditional---------###

def p_conditionals(t):
    '''conditional : con_if
                   | con_switch'''
    t[0] = t[1]

def p_conditional_if(t):
    'con_if : res_if tk_par_o expression tk_par_c tk_key_o instructions tk_key_c'
    t[0] = If(t[3], t[6], None, None, t.lineno(1), find_column(input, t.slice[1]))

def p_conditional_if_else(t):
    'con_if : res_if tk_par_o expression tk_par_c tk_key_o instructions tk_key_c res_else tk_key_o instructions tk_key_c'
    t[0] = If(t[3], t[6], t[10], None, t.lineno(1), find_column(input, t.slice[1]))

def p_conditional_if_else_if(t):
    'con_if : res_if tk_par_o expression tk_par_c tk_key_o instructions tk_key_c res_else con_if'
    t[0] = If(t[3], t[6], None, t[9], t.lineno(1), find_column(input, t.slice[1]))


def p_conditional_switch_default(t):
    'con_switch : res_switch tk_par_o expression tk_par_c tk_key_o default tk_key_c'
    t[0] = Switch(t[3], None, t[6], t.lineno(1), find_column(input, t.slice[1]))

def p_conditional_switch_case(t):
    'con_switch : res_switch tk_par_o expression tk_par_c tk_key_o list_case tk_key_c'
    t[0] = Switch(t[3], t[6], None, t.lineno(1), find_column(input, t.slice[1]))

def p_conditional_switch(t):
    'con_switch : res_switch tk_par_o expression tk_par_c tk_key_o list_case default tk_key_c'
    t[0] = Switch(t[3], t[6], t[7], t.lineno(1), find_column(input, t.slice[1]))

def p_conditional_switch_list_case(t):
    'list_case : list_case case'
    
    if t[2] != None:
        t[1].append(t[2])
    t[0] = t[1]


def p_conditional_case(t):
    'list_case : case'
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [t[1]]

def p_case(t):
    'case : res_case expression tk_twodot instructions'

    t[0] = Case(t[2], t[4], t.lineno(1), find_column(input, t.slice[1]))


def p_default(t):
    'default : res_default tk_twodot instructions'
    t[0] = t[3]


###---------Production Loops---------###

def p_loops(t):
    '''loops : loop_while
             | loop_for'''

    t[0] = t[1]


def p_loops_while(t):
    'loop_while : res_while tk_par_o expression tk_par_c tk_key_o instructions tk_key_c'

    t[0] = While(t[3], t[6], t.lineno(1), find_column(input, t.slice[1]))

def p_loops_for(t):
    'loop_for : res_for tk_par_o for_init tk_dotcomma expression tk_dotcomma for_advance tk_par_c tk_key_o instructions tk_key_c'

    t[0] = For(t[3], t[5], t[7], t[10], t.lineno(1), find_column(input, t.slice[1]))

def p_loops_for_init(t):
    '''for_init : statement
                | assignment'''
    
    t[0] = t[1]

def p_loops_for_advance(t):
    '''for_advance : inc_dec
                   | assignment'''

    t[0] = t[1]


###---------Production Transfers---------###

def p_transfer_break(t):
    'transfer : res_break'
    t[0] = Break(t.lineno(1), find_column(input, t.slice[1]))


###---------Production Type---------###

def p_type(t):
    '''type : res_int
            | res_char
            | res_string
            | res_double
            | res_boolean'''

    if t[1] == 'int':
        t[0] = type.INTEGGER
    elif t[1] == 'double':
        t[0] = type.FLOAT
    elif t[1] == 'char':
        t[0] = type.CHAR
    elif t[1] == 'string':
        t[0] = type.STRING
    elif t[1] == 'boolean':
        t[0] = type.BOOLEAN




###---------Production ptcommaP---------###

def p_ptcommaP(t):
    '''ptcommaP : tk_dotcomma
                | empty'''
    t[0] = t[1]


###---------Production Expression---------###

def p_grouping_expression(t):
    'expression : tk_par_o expression tk_par_c'
    t[0] = t[2]

def p_expression_binary(t):
    '''expression : expression tk_add expression
                  | expression tk_sub expression
                  | expression tk_mult expression
                  | expression tk_div expression
                  | expression tk_module expression
                  | expression tk_pow expression
                  | expression tk_equals expression
                  | expression tk_different expression
                  | expression tk_greater expression
                  | expression tk_greater_equals expression
                  | expression tk_less expression
                  | expression tk_less_equals expression
                  | expression tk_and expression
                  | expression tk_or expression'''
    
    if t[2] == '+':
        t[0] = Arithmetic(t[1], t[3], Arithmetic_Operator.ADDITION, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-':
        t[0] = Arithmetic(t[1], t[3], Arithmetic_Operator.SUBSTRACTION, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '*':
        t[0] = Arithmetic(t[1], t[3], Arithmetic_Operator.MULTIPLICATION, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '/':
        t[0] = Arithmetic(t[1], t[3], Arithmetic_Operator.DIVISION, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '%':
        t[0] = Arithmetic(t[1], t[3], Arithmetic_Operator.MODULS, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '**':
        t[0] = Arithmetic(t[1], t[3], Arithmetic_Operator.POWER, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '==':
        t[0] = Relational(t[1], t[3], Relational_Operators.EQUAL, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '=!':
        t[0] = Relational(t[1], t[3], Relational_Operators.UNEQUAL, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>':
        t[0] = Relational(t[1], t[3], Relational_Operators.GREATER, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>=':
        t[0] = Relational(t[1], t[3], Relational_Operators.GREATEREQUAL, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<':
        t[0] = Relational(t[1], t[3], Relational_Operators.LESS, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<=':
        t[0] = Relational(t[1], t[3], Relational_Operators.LESSEQUAL, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '&&':
        t[0] = Logic(t[1], t[3], Logical_Operators.AND, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '||':
        t[0] = Logic(t[1], t[3], Logical_Operators.OR, t.lineno(2), find_column(input, t.slice[2]))


def p_expression_unary(t):
    '''expression : tk_sub expression %prec tk_uminus
                  | tk_not expression %prec tk_unot'''
    if t[1] == '-':
        t[0] = Arithmetic(t[2], None, Arithmetic_Operator.UMINUS, t.lineno(1), find_column(input, t.slice[1]))
    if t[1] == '!':
        t[0] = Logic(t[2], None, Logical_Operators.NOT, t.lineno(1), find_column(input, t.slice[1]))

def p_expression_unary_right(t):
    '''expression : expression tk_inc
                  | expression tk_dec'''

    if t[2] == '++':
        t[0] = Arithmetic(t[1], None, Arithmetic_Operator.INC, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '--':
        t[0] = Arithmetic(t[1], None, Arithmetic_Operator.DEC, t.lineno(2), find_column(input, t.slice[2]))

def p_expression_unary_cast(t):
    'expression : tk_par_o type tk_par_c expression %prec tk_fcast'

    t[0] = Casting(t[2], t[4], t.lineno(1), find_column(input, t.slice[1]))

def p_expression_primitive_int(t):
    '''
    expression :  tk_int
    '''
    t[0] = Primitive(type.INTEGGER, t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expression_primitive_float(t):
    'expression : tk_decimal'
    t[0] = Primitive(type.FLOAT, t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expression_primitive_string(t):
    'expression : tk_string'
    t[0] = Primitive(type.STRING, t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expression_primitive_char(t):
    'expression : tk_char'
    t[0] = Primitive(type.CHAR, t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_epression_primitive_bool(t):
    '''expression : res_true
                  | res_false'''
    t[0] = Primitive(type.BOOLEAN, t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expression_primitive_id(t):
    'expression : tk_id'
    t[0] = Identifier(t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expression_primitive_null(t):
    'expression : res_null'
    t[0] = Primitive(type.NULL, t[1], t.lineno(1), find_column(input, t.slice[1]))

###---------Production empty---------###

def p_empty(t):
    'empty : '
    pass

import ply.yacc as yacc
parser = yacc.yacc()


input = ''

def get_errors():
    return errors

def parser(str_input):
    global errors
    global input
    errors = []
    lexer = lex.lex()
    parser = yacc.yacc()

    input = str_input
    return parser.parse(str_input)