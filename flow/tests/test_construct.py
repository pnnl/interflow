import unittest

from flow.construct import *
from flow.reader import *


class TestConstruct(unittest.TestCase):
    """Conduct test for functions of construct.py."""

    def test_construct_nested_dictionary(self):

        # load data
        sample_data = read_data()
        first_region = sample_data[sample_data.columns[0]].iloc[0]
        first_column = sample_data.columns[0]
        sample_data = sample_data.loc[sample_data[first_column] == first_region]

        # test too few columns raises error
        data_few = sample_data.drop(sample_data.columns[0], axis=1)

        with self.assertRaises(ValueError):
            construct_nested_dictionary(df=data_few)

        # test too many columns raises error
        data_extra = sample_data.copy()
        data_extra['a'] = 1
        with self.assertRaises(ValueError):
            construct_nested_dictionary(df=data_extra)

        # test that with the correct data input, the output is a dictionary
        output = construct_nested_dictionary(df=sample_data)
        self.assertTrue(type(output) == dict)

        # test that the output dictionary has the correct number of levels

        


if __name__ == '__main__':
    unittest.main()
