import unittest
from unittest import mock
from urllib.error import URLError

from customer import Customer
from readers import FileReader, HttpReader


def mocked_requests_urlopen(*args, **kwargs):
    """
    Function to mock urllib.request.urlopen function
    """

    class MockResponse:
        def __init__(self, lines, status_code):
            self.lines = lines
            self.status_code = status_code

        def getcode(self):
            return self.status_code

        def readlines(self):
            return self.lines

    if args[0] == 'http://someurl.com/success.txt':
        lines = [b'the quick brown fox', b'jumps over the lazy', b'dog']
        return MockResponse(lines, 200)
    elif args[0] == 'http://someurl.com/empty.txt':
        return MockResponse([], 200)
    return MockResponse([], 400)


class TestReaders(unittest.TestCase):
    """
    Testing readers and Customer creation from json
    """

    def test_file_reader_empty(self):
        path = 'resources/test/empty.txt'
        content = FileReader.read(path)
        correct_list = []
        self.assertListEqual(content, correct_list)

    def test_file_reader_not_found(self):
        path = 'resources/test/not_found.txt'
        self.assertRaises(FileNotFoundError, FileReader.read, path)

    def test_file_reader_found(self):
        path = 'resources/test/some.txt'
        correct_list = ['the quick brown fox', 'jumps over the lazy', 'dog']
        content = FileReader.read(path)
        self.assertListEqual(content, correct_list)

    @mock.patch('urllib.request.urlopen', side_effect=mocked_requests_urlopen)
    def test_http_reader_success(self, mock_urlopen):
        url = "http://someurl.com/success.txt"
        content = HttpReader.read(url)
        correct_list = ['the quick brown fox', 'jumps over the lazy', 'dog']
        self.assertListEqual(content, correct_list)

    @mock.patch('urllib.request.urlopen', side_effect=mocked_requests_urlopen)
    def test_http_reader_fail(self, mock_urlopen):
        url = "http://someurl.com/fail.txt"
        self.assertRaises(URLError, HttpReader.read, url)

    @mock.patch('urllib.request.urlopen', side_effect=mocked_requests_urlopen)
    def test_http_reader_empty(self, mock_urlopen):
        url = "http://someurl.com/empty.txt"
        content = HttpReader.read(url)
        self.assertListEqual([], content)

    def test_customer_object_valid_json(self):
        json = '{"latitude": "54.0894797", "user_id": 8, "name": "Eoin Ahearn", "longitude": "-6.18671"}'
        correct_customer = Customer(8, 'Eoin Ahearn', 54.0894797, -6.18671)
        print(correct_customer)
        customer = Customer.json_decoder(json)
        print(customer)
        self.assertEqual(customer, correct_customer)

    def test_customer_object_invalid_json(self):
        json = '{"magnitude": "54.0894797", "user_id": 8, "name": "Eoin Ahearn", "longitude": "-6.18671"}'
        self.assertRaises(KeyError, Customer.json_decoder, json)

        json = '{"user_id": 8, "name": "Eoin Ahearn", "longitude": "-6.18671"}'
        self.assertRaises(KeyError, Customer.json_decoder, json)
