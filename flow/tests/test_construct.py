import unittest

from flow.construct import *
from flow.reader import *


class TestConstruct(unittest.TestCase):
    """Conduct test for functions of construct.py."""

    def test_construct_nested_dictionary(self):

        # load data
        data = read_data()

        # test too few columns raises error
        data_few = data.drop(data.columns[0], axis=1)

        with self.assertRaises(ValueError):
            construct_nested_dictionary(df=data_few)


if __name__ == '__main__':
    unittest.main()
