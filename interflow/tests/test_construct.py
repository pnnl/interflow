import unittest
from interflow.construct import *
from interflow.reader import *


class TestConstruct(unittest.TestCase):
    """Conduct tests for functions of construct.py."""

    def test_construct_nested_dictionary(self):

        # load data
        sample_data = read_sample_data()

        # grab a subset of the sample
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
        def calc_dictionary_levels(d: dict):
            nest_count = max(calc_dictionary_levels(v) if isinstance(v, dict) else 0 for v in d.values()) + 1
            return nest_count

        levels_calculated = calc_dictionary_levels(output)
        levels_expected = 15

        self.assertEqual(levels_calculated, levels_expected)


if __name__ == '__main__':
    unittest.main()
