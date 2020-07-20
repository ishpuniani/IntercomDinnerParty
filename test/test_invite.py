import sys
import unittest
from io import StringIO
from json import JSONDecodeError
from unittest import mock

import main
from customer import Customer


class TestInvite(unittest.TestCase):
    """
    Testing the behaviour of the program with invalid configurations.
    """

    def test_config_empty(self):
        # Testing empty config file
        config_path = 'resources/test/configs/config_empty.json'
        self.assertRaises(JSONDecodeError, main.execute, config_path)

    def test_config_missing(self):
        # Testing missing config file
        config_path = 'resources/test/configs/config_not_found.json'
        self.assertRaises(FileNotFoundError, main.execute, config_path)

    def test_config_missing_keys(self):
        # Testing missing keys
        config_path = 'resources/test/configs/config_invalid.json'
        self.assertRaises(KeyError, main.execute, config_path)

    def test_config_valid(self):
        """
        An end to end test for the entire program. On the basis of the config, only one customer should be returned.
        """
        config_path = 'resources/test/configs/config_test.json'
        invited_customers = main.execute(config_path)
        self.assertEqual(1, len(invited_customers))

        cust_json = '{"latitude": "54.0894797", "user_id": 8, "name": "Eoin Ahearn", "longitude": "-6.18671"}'
        customer = Customer.json_decoder(cust_json)
        self.assertEqual(invited_customers[0], customer)

    def test_duplicate_customers(self):
        """
        The customer file contains duplicate customers.
        The invite file should contain only the
        """
        config_path = 'resources/test/configs/config_test_dup.json'
        invited_customers = main.execute(config_path)
        self.assertEqual(1, len(invited_customers))

        cust_json = '{"latitude": "54.0894797", "user_id": 8, "name": "Eoin Ahearn", "longitude": "-6.18671"}'
        customer = Customer.json_decoder(cust_json)
        self.assertEqual(invited_customers[0], customer)

    def test_different_customer_distance_ranges(self):
        """
        Testing customer within the different distance ranges
        """
        config_path = 'resources/test/configs/config_test_150.json'
        invited_customers = main.execute(config_path)
        self.assertEqual(2, len(invited_customers))

        config_path = 'resources/test/configs/config_test_200.json'
        invited_customers = main.execute(config_path)
        self.assertEqual(4, len(invited_customers))

        config_path = 'resources/test/configs/config_test_500.json'
        invited_customers = main.execute(config_path)
        self.assertEqual(7, len(invited_customers))
