#!/usr/bin/env python3
"""In this task you will write the first unit test
for utils.access_nested_map.Create a TestAccessNestedMap
class that inherits from unittest.TestCase.Implement the
TestAccessNestedMap.test_access_nested_map method to test
that the method returns what it is supposed to.Decorate
the method with @parameterized.expand to test the function
for following inputs:

    nested_map={"a": 1}, path=("a",)
    nested_map={"a": {"b": 2}}, path=("a",)
    nested_map={"a": {"b": 2}}, path=("a", "b")
For each of these inputs, test with assertEqual that the
function returns the expected result.The body of the test method
should not be longer than 2 lines."""

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """test the access nested map function"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """test the access nested map method"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """check that a KeyError is raised when the
        access_nested_map function is called with these parameters
        """
        with self.assertRaises(KeyError) as err:
            access_nested_map(nested_map, path)
        self.assertEqual(f"KeyError('{expected}')", repr(err.exception))


if __name__ == "__main__":
    unittest.main()
