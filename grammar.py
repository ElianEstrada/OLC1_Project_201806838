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
    "var": "var"

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
    r'\'\\?.\''
    t.value = t.value[1:-1]

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


import ply.lex as lex

def analize_lex(string): 
    current = lex.lex()
    current.input(string)
    nuevo = current.token()
    print(nuevo)
    while nuevo != None:
        nuevo = current.token()
        print(nuevo)

