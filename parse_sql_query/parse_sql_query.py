#!/usr/bin/env python
from ply_files import parser


def parse_sql_query(query, data=None):
    # Call the parser.
    # Get the response
    # Filter out all the unwanted data elements.
    parse_resp = parser(query, data=data)

    resp_list = []
    for i in xrange(len(data)):
        if parse_resp[i] is True:
            resp_list.append(data[i])

    return resp_list
