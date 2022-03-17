import unittest
from interflow.sample_data import *


class MyTestCase(unittest.TestCase):
    """Conduct tests for functions of sample_data.py."""

    def test_convert_kwh_bbtu(self):

        # test that the outcome is as expected
        output = convert_kwh_bbtu(500)
        expected = 0.00170607

        self.assertEqual(output, expected)

    def test_convert_mwh_bbtu(self):

        # test that the outcome is as expected
        output = convert_mwh_bbtu(500)
        expected = 1.706

        self.assertEqual(output, expected)

if __name__ == '__main__':
    unittest.main()
