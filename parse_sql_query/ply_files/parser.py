#!/usr/bin/env python

# TODO: Change imports to package level
import ply.yacc as yacc
from lexer import lexer

# Needed for parser to obtain tokens explicitly
from lexer import tokens

'''

            GRAMMAR
|---------------------------------|
|    Z : L_PAREN Z R_PAREN        |
|      | Z LOGICAL Z              |
|      | Z COMPARISION Z          |
|      | FIELDS                   |
|      | LITERALS                 |
|                                 |
|    LOGICAL : NOT                |
|            | AND                |
|            | OR                 |
|                                 |
|    COMPARISION : EQUALS         |
|                | NOT_EQUALS     |
|                | GT             |
|                | LT             |
|                | GTE            |
|                | LTE            |
|---------------------------------|


ALITER:

P : L_PAREN E R_PAREN
  | E

E : E LOGICAL E
  | C

C : T COMPARISION T
  | T

T : FIELDS
  | LITERALS

'''

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('nonassoc', 'EQUALS', 'NOT_EQUALS'),
    ('nonassoc', 'GT', 'LT', 'GTE', 'LTE'),
    ('nonassoc', 'L_PAREN', 'R_PAREN'),
)


def p_start_prod(p):
    '''S : Z'''
    p[0] = p[1]


def p_common_prod_paren(p):
    '''
    Z : L_PAREN Z R_PAREN
    '''
    p[0] = p[2]


def p_common_prod_logical_0(p):
    '''
    Z : NOT Z
    '''
    # Probably check if p[2] are boolean
    p[0] = not p[2]


def p_common_prod_logical_1(p):
    '''
    Z : Z AND Z
      | Z OR Z
    '''
    # Probably check if p[1] and p[3] are boolean
    l_op = p[2].lower()
    if l_op == "and":
        p[0] = p[1] and p[3]
    elif l_op == "or":
        p[0] = p[1] or p[3]
    else:
        raise SyntaxError


def p_common_prod_comparision(p):
    '''
    Z : Z EQUALS Z
      | Z NOT_EQUALS Z
      | Z GT Z
      | Z LT Z
      | Z GTE Z
      | Z LTE Z
    '''
    # Do some kind of logical processing here.
    l_op = p[1]
    r_op = p[3]

    if p[2] == "=":
        p[0] = l_op == r_op
    elif p[2] == "!=":
        p[0] = l_op != r_op
    elif p[2] == ">":
        p[0] = l_op > r_op
    elif p[2] == "<":
        p[0] = l_op < r_op
    elif p[2] == ">=":
        p[0] = l_op >= r_op
    elif p[2] == "<=":
        p[0] = l_op <= r_op
    else:
        raise SyntaxError


def p_common_prod_terminal(p):
    '''
    Z : FIELDS
      | LITERALS
    '''
    p[0] = p[1]


def p_error(p):
    if p:
        print p
        print ("Syntax Error - %s" % p.value)
    else:
        print ("Syntax Error at EOF")

yacc.yacc()

if __name__ == "__main__":
    # This is just for the PEP8 warning to go away :P
    # TODO: Remove this
    tokens
    s = '''a < z'''
    print yacc.parse(s, lexer=lexer)
