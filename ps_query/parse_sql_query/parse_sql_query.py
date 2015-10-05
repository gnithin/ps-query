#!/usr/bin/env python
from ply_files import parser


def clean_data(data):
    # TODO: clean data(Do not change order)
    new_data = []

    for li_ele in data:
        d = {}
        for k, v in li_ele.iteritems():
            # Add condition for data
            # Key processing
            d_key = k.lower()

            # Value processing
            if d_key == "name":
                v = v.strip("/")

            d[d_key] = v
        new_data.append(d)

    return new_data


def parse_sql_query(query, data=None):
    # Call the parser.
    # Get the response
    # Filter out all the unwanted data elements.

    cleaned_data = clean_data(data)
    parse_resp = parser(query, data=cleaned_data)

    resp_list = []
    for i in xrange(len(data)):
        if parse_resp[i] is True:
            resp_list.append(data[i])

    return resp_list
