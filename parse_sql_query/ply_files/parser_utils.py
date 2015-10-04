import re
from .name_mapper import datetime_type_fields
from dateutil.parser import parse as datetime_parser


def middleware(func_name):
    def callback(*args, **kwargs):
        if 'type_data' in kwargs:
            l_op = args[0]
            r_op = args[1]

            # Handling datetime
            type_data = kwargs['type_data']
            type_list = [v
                         for l in type_data
                         for k, v in l.iteritems()
                         if k == "val"
                         ]

            # Any kind of preprocessing before the actual processing
            # needs to be done here
            # The types can be gauged by checking out the type_data list
            #
            if any([t in datetime_type_fields for t in type_list]):
                # perform datetime conversions
                l_op, r_op = convert_datetime(l_op, r_op)

        return func_name(l_op, r_op)
    return callback

# Functions that convert the input field values


def convert_datetime(op1, op2):
    def get_secs(t):
        return datetime_parser(t).strftime("%s")

    # handle all datetime stuff here.
    # Listing the datetimes that need to be considered.
    # 2015-09-14T20:03:19.973324053Z
    # TODO: use [parseddatetime](https://github.com/bear/parsedatetime)
    # 2015-09-14 00:00:00 - Mysql format -> YYYY-MM-DD HH:MM:SS
    # yesterday
    # tomorrow
    # today
    op1, op2 = get_secs(op1), get_secs(op2)
    return op1, op2

# Functions that describe the functioning of an operator


def logic_optr_NOT_EQUALS(l_op, r_op):
    resp_val = l_op != r_op
    return resp_val


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


def logic_optr_like(comparator, regex):
    # Helper function for matching queries
    def match_regex(comp, r):
        # This is done to make sure that the whole term is matched.
        # Might need to remove this block if needed.
        if r[0] != "^":
            r = r'^' + r
        if r[-1] != "$":
            r += r'$'
        return re.match(r, comp) is not None

    resp_val = False

    if type(comparator) == list:
        for c in comparator:
            if match_regex(c, regex):
                resp_val = True
                break
    else:
        resp_val = match_regex(comparator, regex)

    return resp_val


@middleware
def logic_optr_GT(l_op, r_op, type_data=None):
    resp_val = l_op > r_op
    return resp_val


@middleware
def logic_optr_LT(l_op, r_op, type_data=None):
    resp_val = l_op < r_op
    return resp_val


def logic_optr_GTE(l_op, r_op, type_data=None):
    resp_val = l_op >= r_op
    return resp_val


def logic_optr_LTE(l_op, r_op, type_data=None):
    resp_val = l_op <= r_op
    return resp_val
