import re


def logic_optr_EQUALS(l_op, r_op):
    l_list_bool = type(l_op) == list
    r_list_bool = type(r_op) == list

    # The following takes into account the presence of lists
    # as the items to be compared.
    # If both the operands are strings, or if both the operands
    # are lists, perform direct comparision.
    # If only one of them is a list, then all the list elements
    # are searched.(For eg, `command` is a list of commands, so search
    # is performed for all keywords)

    if (
        (l_list_bool and r_list_bool) or
        (not l_list_bool and not r_list_bool)
    ):
        resp_val = l_op == r_op

    # TODO: Clean this ugly piece of shit(Use a helper function)
    else:
        # if either one of the operands is a list
        resp_val = False
        op1, op2 = (l_op, r_op) \
            if type(l_op) == list \
            else (r_op, l_op)

        for e in op1:
            if e == op2:
                resp_val = True
                break

    return resp_val


# Helper function
def match_regex(comparator, regex):
    regex = r'^' + regex + r'$'
    return re.match(regex, comparator) is not None


def logic_optr_like(comparator, regex):
    resp_val = match_regex(comparator, regex)
    return resp_val