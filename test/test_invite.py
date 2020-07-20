import unittest
from json import JSONDecodeError

import main
from customer import Customer


class TestInvite(unittest.TestCase):
    """
    Testing the behaviour of the program with invalid configurations.
    """

    def test_config_empty(self):
        # Testing empty config file
        config_path = 'resources/test/config_empty.json'
        self.assertRaises(JSONDecodeError, main.execute, config_path)

    def test_config_missing(self):
        # Testing missing config file
        config_path = 'resources/test/config_not_found.json'
        self.assertRaises(FileNotFoundError, main.execute, config_path)

    def test_config_missing_keys(self):
        # Testing missing keys
        config_path = 'resources/test/config_invalid.json'
        self.assertRaises(KeyError, main.execute, config_path)

    def test_config_valid(self):
        config_path = 'resources/test/config_test.json'
        invited_customers = main.execute(config_path)
        self.assertEqual(1, len(invited_customers))

        cust_json = '{"latitude": "54.0894797", "user_id": 8, "name": "Eoin Ahearn", "longitude": "-6.18671"}'
        customer = Customer.json_decoder(cust_json)
        self.assertEqual(invited_customers[0], customer)

    def test_duplicate_customers(self):
        pass

    def test_different_customer_ranges(self):
        pass
