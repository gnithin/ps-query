from ps_query import ps_query

import unittest
import re
from dateutil.parser import parse as datetime_parser

test_func = ps_query.get_container_details

# TODO: Think about creating a list of containers
# that would emulate the test properly.


def get_secs(t):
    '''
    Helper function for converting string time into seconds
    '''
    return datetime_parser(t).strftime("%s")


class TestPSQueryBasicFunctions(unittest.TestCase):
    def test_date_1(self):
        date_str = "2015-09-14 16:42:45"
        conv_date_secs = get_secs(date_str)
        query = ("created > '%s'" % date_str)
        arg = "a"
        resp, status = test_func(
            arg,
            query
        )

        # Asserting non-zero amount of responses.
        self.assertGreater(len(resp), 0)
        for e in resp:
            # Convert to time
            self.assertGreater(get_secs(e["Created"]), conv_date_secs)

    def test_date_2(self):
        date_str = "2015-09-14 16:42:45"
        conv_date_secs = get_secs(date_str)
        query = ("created = '%s'" % date_str)
        arg = "a"
        resp, status = test_func(
            arg,
            query
        )

        # Asserting non-zero amount of responses.
        self.assertGreater(len(resp), 0)
        for e in resp:
            # Convert to time
            self.assertEqual(get_secs(e["Created"]), conv_date_secs)

    def test_regex(self):
        regex = '.*(lee|lly).*'
        query = ('name like "%s"' % regex)
        arg = "a"
        resp, status = test_func(
            arg,
            query
        )

        for e in resp:
            regex_res = re.match(regex, e["Name"])
            self.assertEqual(True, regex_res is not None)

    def test_name_equal(self):
        key = 'sleepy_einstein'
        query = ('name = "%s"' % key)
        arg = "a"
        resp, status = test_func(
            arg,
            query
        )
        for e in resp:
            self.assertEqual(e["Name"], '/' + key)

    def test_empty(self):
        query = ""
        arg = "a"

        resp, status = test_func(
            arg,
            query
        )

        self.assertTrue(resp)

if __name__ == "__main__":
    unittest.main()
