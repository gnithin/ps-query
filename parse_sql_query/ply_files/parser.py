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

    # Parenthesis
    'L_PAREN',
    'R_PAREN'
)

# Regex specifications

t_NOT = r'[nN][oO][tT]'
t_AND = r'[aA][nN][dD]'
t_OR = r'[oO][rR]'

t_EQUALS = r'='
t_NOT_EQUALS = r'!='
t_GT = r'>'
t_LT = r'<'
t_GTE = r'>='
t_LTE = r'<='
t_L_PAREN = r'\('
t_R_PAREN = r'\)'

t_ignore = ' \t'


literal_lb = r'.*?(?<!\\)'
literal_regex = r'' + (r""""{0}"|'{0}'""".format(literal_lb))
print literal_regex


# @TOKEN(literal_regex)
@TOKEN(r'".*(?<!\\)"')
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

if __name__ == "__main__":
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
        name = "A Leftie's \"Nightmare\""
        ''',
        # Testing operations
        '''
        name = 'aladdin' and occupation = 'street rat'
        '''
    ]

    for data in test_data_li:
        lexer.input(data)
        for tok in lexer:
            print tok
        print "-"*20
