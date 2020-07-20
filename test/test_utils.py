import unittest

from readers import FileReader
from utils import Utils


class TestUtils(unittest.TestCase):
    """
    Testing utility functions
    """
    def test_write_to_file(self):
        """
        Testing write to file
        Writing and array to file and then reading the files and comparing if they have been written properly
        :return:
        """
        content = ['the quick brown fox', 'jumps over the lazy', 'dog']
        filepath = 'resources/test/out/write.txt'
        Utils.write_to_file(filepath, content)
        read_content = FileReader.read(filepath)
        self.assertEqual(content, read_content)

    def test_circle_distance(self):
        """
        Test correct distance is calculated in function between Galway and Dublin using
        Google Maps calculated distance as the reference value to be asserted against
        """

        galway_coords = (53.2707, -9.0568)
        dublin_coords = (53.3498, -6.2603)
        google_maps_calc_distance = 185.99
        distance = Utils.great_circle_distance(galway_coords, dublin_coords)

        self.assertEqual(google_maps_calc_distance, distance)
