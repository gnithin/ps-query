#!/usr/bin/env python

# TODO: Change imports to package level
import ply.yacc as yacc
from lexer import lexer

# Needed for parser to obtain tokens explicitly
from lexer import tokens
from .name_mapper import name_map
import parser_utils as p_utils

meta_data = None

# Some constants
LITERALS = 0
FIELDS = 1


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
    ('nonassoc', 'GT', 'LT', 'GTE', 'LTE', 'LIKE'),
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
    resp_table = []
    for i in len(p[2]):
        resp_table.append(not p[2][i])
    p[0] = resp_table


def p_common_prod_logical_1(p):
    '''
    Z : Z AND Z
      | Z OR Z
    '''
    # TODO: Probably check if p[1] and p[3] are boolean
    optr = p[2].lower()
    resp_table = []

    for i in xrange(len(p[1])):
        l_val = p[1][i]
        r_val = p[3][i]

        if optr == "and":
            resp_val = l_val and r_val
        elif optr == "or":
            resp_val = l_val or r_val
        else:
            raise SyntaxError
        resp_table.append(resp_val)

    p[0] = resp_table


def p_common_prod_comparision(p):
    '''
    Z : Z EQUALS Z
      | Z NOT_EQUALS Z
      | Z GT Z
      | Z LT Z
      | Z GTE Z
      | Z LTE Z
      | Z LIKE Z
    '''
    # Do some kind of logical processing here.
    l_key = p[1]['val']
    r_key = p[3]['val']

    l_type = p[1]['type']
    r_type = p[3]['type']

    optr = p[2]

    if len(meta_data) == 0:
        raise SyntaxError

    # Check if the literal values are in the meta_data
    # TODO: `not in first_row` needs to be standardized
    first_row = meta_data[0]

    if (
        r_type == FIELDS and
        r_key not in first_row.keys()
    ) or (
        l_type == FIELDS and
        l_key not in first_row.keys()
    ):
        # Raise some meaningful error
        raise SyntaxError

    # This var is for detecting the type of variable
    operations_list = []
    if r_type == FIELDS:
        operations_list.append({
            "pos"   :   "r",
            "val"   :   r_key
        })
    if l_type == FIELDS:
        operations_list.append({
            "pos"   :   "l",
            "val"   :   l_key
        })

    resp_table = []

    '''
    Iterate through each element in `meta_data`,
    Get the value of the key that is used in the query,
    Resolve the comparision operations.
    '''
    for data in meta_data:
        l_op = data[l_key] if l_type == FIELDS else l_key
        r_op = data[r_key] if r_type == FIELDS else r_key

        resp_val = None

        # TODO: Do this better(how to do this without eval/ast_eval?)
        if optr == "=":
            resp_val = p_utils.logic_optr_EQUALS(l_op, r_op)
        elif optr == "!=":
            resp_val = p_utils.logic_optr_NOT_EQUALS(l_op, r_op)
        elif optr == ">":
            resp_val = p_utils.logic_optr_GT(
                l_op,
                r_op,
                type_data=operations_list
            )
        elif optr == "<":
            resp_val = p_utils.logic_optr_LT(
                l_op,
                r_op,
                type_data=operations_list
            )
        elif optr == ">=":
            resp_val = p_utils.logic_optr_GTE(l_op, r_op)
        elif optr == "<=":
            resp_val = p_utils.logic_optr_LTE(l_op, r_op)
        elif optr.lower() == "like":
            # Find the literal(regex)
            comparator = r_op
            regex = l_op
            if r_type == LITERALS and l_type == FIELDS:
                comparator = l_op
                regex = r_op

            resp_val = p_utils.logic_optr_like(comparator, regex)

        else:
            raise SyntaxError
        resp_table.append(resp_val)

    p[0] = resp_table


def p_common_prod_field(p):
    '''
    Z : FIELDS
    '''

    val = p[1]
    if val in name_map.keys():
        val = name_map[val]

    p[0] = {
        "type"  :   FIELDS,
        "val"   :   val
    }


def p_common_prod_literal(p):
    '''
    Z : LITERALS
    '''
    p[0] = {
        "type"  :   LITERALS,
        "val"   :   p[1]
    }


def p_error(p):
    if p:
        print p
        print ("Syntax Error - %s" % p.value)
    else:
        print ("Syntax Error at EOF")

yacc.yacc()


def parser(query, data=None):
    global meta_data
    meta_data = data

    yacc_resp = yacc.parse(query, lexer=lexer)
    return yacc_resp

if __name__ == "__main__":
    # This is just for the PEP8 warning to go away :P
    # TODO: Remove this
    tokens
    s = '''a < z'''
    print yacc.parse(s, lexer=lexer)
