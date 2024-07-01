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
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json


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
        with self.assertRaises(expected) as context:
            access_nested_map(nested_map, path)
        # self.assertEqual(f"KeyError('{expected}')", repr(err.exception))


class TestGetJson(unittest.TestCase):
    """tests get_json function"""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, expected):
        """test that utils.get_json returns the expected result"""
        mock_response = Mock()
        mock_response.json.return_value = expected
        with patch('requests.get', return_value=mock_response):
            response = get_json(test_url)

            self.assertEqual(response, expected)


if __name__ == "__main__":
    unittest.main()
