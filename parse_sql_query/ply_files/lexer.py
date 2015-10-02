#!/usr/bin/env python

import ply.lex as lex
# import ply.yacc as yacc
from ply.lex import TOKEN

tokens = (
    'FIELDS',
    'LITERALS',  # String literals only

    # Logical operators
    'NOT',
    'AND',
    'OR',

    # Comparision operators
    'EQUALS',
    'NOT_EQUALS',
    'GT',
    'LT',
    'GTE',
    'LTE',
    'LIKE',

    # Parenthesis
    'L_PAREN',
    'R_PAREN'
)

# Regex specifications


t_EQUALS = r'='
t_NOT_EQUALS = r'!='
t_GT = r'>'
t_LT = r'<'
t_GTE = r'>='
t_LTE = r'<='

t_L_PAREN = r'\('
t_R_PAREN = r'\)'

# Ignoring spaces and tabs
t_ignore = ' \t'

# The literal regex needs to account for "DOUBLE-QUOTE" and 'SINGLE-QUOTE' as
# well
literal_lb = r'.*?(?<!\\)'
literal_regex = r'"{0}"|\'{0}\''.format(literal_lb)


@TOKEN(r'[nN][oO][tT]')
def t_NOT(t):
    return t


@TOKEN(r'[aA][nN][dD]')
def t_AND(t):
    return t


@TOKEN(r'[oO][rR]')
def t_OR(t):
    return t


@TOKEN(r'[lL][iI][kK][eE]')
def t_LIKE(t):
    return t


@TOKEN(literal_regex)
def t_LITERALS(t):
    t.value = t.value[1:-1]
    return t


@TOKEN(r'[\w.]+')
def t_FIELDS(t):
    return t


@TOKEN(r'\n')
def t_newline(t):
    t.lexer.lineno += len(t.value)


def t_error(t):
    print ("Lexer Error! %s" % str(t))
    t.lexer.skip(1)


lexer = lex.lex()

# -----------------------------------------------------------------------------


# Function to test the lexer(Needs to be called by __main__ only)
def test_lexer():
    # Testing the lexer
    test_data_li = [
        # Testing basic literals an dfields
        '''
        name = "asdasd"
        ''',
        '''
        created_date > '2007'
        ''',
        '''
        name = "A Leftie's \\"Nightmare\\""
        ''',
        # Testing operations
        '''
        name = 'aladdin' and occupation = 'street rat'
        ''',
        '''c''',
        '''command or and not like askhdajs "asas"'''
    ]

    for data in test_data_li:
        lexer.input(data)
        for tok in lexer:
            print tok
        print "-"*20

if __name__ == "__main__":
    test_lexer()
