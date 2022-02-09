import unittest
import pandas as pd
from flow.deconstruct import *
from flow.reader import *
from flow.calc_flow import *


class TestDeconstruct(unittest.TestCase):
    """Conduct test for functions of deconstruct.py."""

    def test_deconstruct_dictionary(self):

        # create a sample nested dictionary to test with
        level5_dict = {'region1_T1_T2_T3_T4_T5_to_S1_S2_S3_S4_S5_units': 100}

        # test that with the correct data input, the output is a dataframe
        output = deconstruct_nested_dictionary(level5_dict)
        self.assertTrue(type(output) == pd.DataFrame)


if __name__ == '__main__':
    unittest.main()
