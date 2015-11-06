from ps_query import ps_query
import test_utils

import unittest
import re

test_func = ps_query.get_container_details

# TODO: Think about creating a list of containers
# that would emulate the test properly.
# Right now, it will only work for the docker history in my
# PC :D


class TestPSQueryBasicFunctions(unittest.TestCase):
    def test_or_operation(self):
        name = "silly_leakey"
        created = "2015-09-14"
        created_secs = test_utils.get_secs(created)
        query = (
            "name = '%s' or created > '%s'"
            %
            (name, created)
        )
        arg = "a"
        resp, status = test_func(
            arg,
            query
        )

        self.assertGreater(len(resp), 0)

        for e in resp:
            cond = (
                e["Name"] == ("/%s" % name) or
                test_utils.get_secs(e["Created"]) > created_secs
            )
            self.assertTrue(cond)

    def test_and_operation_1(self):
        query = "name = 'silly_leakey' and created > '2015-09-14'"
        arg = "a"
        resp, status = test_func(
            arg,
            query
        )

        self.assertEqual(len(resp), 0)

    def test_and_operation_2(self):
        query = "name = 'silly_leakey' and created < '2015-09-14'"
        arg = "a"
        resp, status = test_func(
            arg,
            query
        )

        self.assertGreater(len(resp), 0)

    def test_date_1(self):
        date_str = "2015-09-14 16:42:45"
        conv_date_secs = test_utils.get_secs(date_str)
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
            self.assertGreater(
                test_utils.get_secs(e["Created"]),
                conv_date_secs
            )

    def test_date_2(self):
        date_str = "2015-09-14 16:42:45"
        conv_date_secs = test_utils.get_secs(date_str)
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
            self.assertEqual(test_utils.get_secs(e["Created"]), conv_date_secs)

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
            self.assertTrue(regex_res is not None)

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
