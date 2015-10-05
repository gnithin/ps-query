import sys

# Probably need this at every test file
if ".." not in sys.path:
    sys.path.insert(0, "..")

from ps_query import ps_query

import unittest

test_func = ps_query.get_container_details


class TestPSQueryBasicFunctions(unittest.TestCase):

    def test_name_equal(self):
        key = 'sleepy_einstein'
        query = ('name = "%s"' % key)
        arg = "a"
        resp = test_func(
            arg,
            query
        )
        for e in resp:
            self.assertEqual(e["Name"], '/' + key)

    def test_empty(self):
        query = ""
        arg = "a"

        resp = test_func(
            arg,
            query
        )

        self.assertTrue(resp)

if __name__ == "__main__":
    unittest.main()
