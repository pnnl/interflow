import unittest
from interflow.deconstruct import *
from interflow.calc_flow import *


class TestDeconstruct(unittest.TestCase):
    """Conduct tests for functions of deconstruct.py."""

    def test_deconstruct_dictionary(self):

        # create a sample level5 dictionary to test with
        level5_dict = {'region1_T1_T2_T3_T4_T5_to_S1_S2_S3_S4_S5_units': 100}

        # test that with the correct data input, the output is a dataframe
        output5 = deconstruct_dictionary(level5_dict)
        self.assertTrue(type(output5) == pd.DataFrame)

        # test that the output dataframe has the correct columns if a level 5 name is passed
        col5 = ['region', 'S1', 'S2', 'S3','S4', 'S5', 'T1', 'T2', 'T3','T4', 'T5', 'units', 'value']
        output_columns5 = output5.columns.to_list()
        self.assertEqual(col5, output_columns5)

        # test that the 'to' column is not in the output DataFrame
        output5_column_list = output5.columns.to_list()
        not_in_list = "to" not in output5_column_list
        self.assertTrue(not_in_list)

        # no null data rows
        rows_with_null = [index for index, row in output5.iterrows() if row.isnull().any()]
        self.assertEqual(rows_with_null, [])

        # create a sample level4 dictionary to test with
        level4_dict = {'region1_T1_T2_T3_T4_to_S1_S2_S3_S4_units': 100}

        # test that the output dataframe has the correct columns if a level 5 name is passed
        col4 = ['region', 'S1', 'S2', 'S3', 'S4', 'T1', 'T2', 'T3', 'T4', 'units', 'value']
        output4 = deconstruct_dictionary(level4_dict)
        output_columns4 = output4.columns.to_list()
        self.assertEqual(col4, output_columns4)

        # test that the 'to' column is not in the output4 DataFrame
        output4_column_list = output4.columns.to_list()
        not_in_list = "to" not in output4_column_list
        self.assertTrue(not_in_list)

        # no null data rows
        rows_with_null = [index for index, row in output4.iterrows() if row.isnull().any()]
        self.assertEqual(rows_with_null, [])

        # create a sample level3 dictionary to test with
        level3_dict = {'region1_T1_T2_T3_to_S1_S2_S3_units': 100}

        # test that the output dataframe has the correct columns if a level 5 name is passed
        col3 = ['region', 'S1', 'S2', 'S3', 'T1', 'T2', 'T3', 'units', 'value']
        output3 = deconstruct_dictionary(level3_dict)
        output_columns3 = output3.columns.to_list()
        self.assertEqual(col3, output_columns3)

        # test that the 'to' column is not in the output3 DataFrame
        output3_column_list = output3.columns.to_list()
        not_in_list = "to" not in output3_column_list
        self.assertTrue(not_in_list)

        # no null data rows
        rows_with_null = [index for index, row in output3.iterrows() if row.isnull().any()]
        self.assertEqual(rows_with_null, [])

        # create a sample level2 dictionary to test with
        level2_dict = {'region_T1_T2_to_S1_S2_units': 100}

        # test that the output dataframe has the correct columns if a level 5 name is passed
        col2 = ['region', 'S1', 'S2', 'T1', 'T2', 'units', 'value']
        output2 = deconstruct_dictionary(level2_dict)
        output_columns2 = output2.columns.to_list()
        self.assertEqual(col2, output_columns2)

        # test that the 'to' column is not in the output2 DataFrame
        output2_column_list = output2.columns.to_list()
        not_in_list = "to" not in output2_column_list
        self.assertTrue(not_in_list)

        # no null data rows
        rows_with_null = [index for index, row in output2.iterrows() if row.isnull().any()]
        self.assertEqual(rows_with_null, [])

        # create a sample level1 dictionary to test with
        level1_dict = {'region_T1_to_S1_units': 100}

        # test that the output dataframe has the correct columns if a level 5 name is passed
        col1 = ['region', 'S1', 'T1','units', 'value']
        output1 = deconstruct_dictionary(level1_dict)
        output_columns1 = output1.columns.to_list()
        self.assertEqual(col1, output_columns1)

        # test that the 'to' column is not in the output1 DataFrame
        output1_column_list = output1.columns.to_list()
        not_in_list = "to" not in output1_column_list
        self.assertTrue(not_in_list)

        # no null data rows
        rows_with_null = [index for index, row in output1.iterrows() if row.isnull().any()]
        self.assertEqual(rows_with_null, [])

        # create a sample level dictionary with too many variable naming levels
        level6_dict = {'region1_T1_T2_T3_T4_T5_T6_to_S1_S2_S3_S4_S5_units': 100}

        # test that having too many underscore separated names in the key raises a ValueError
        with self.assertRaises(ValueError):
            deconstruct_dictionary(level6_dict)

        # create a sample level dictionary with too few variable naming levels
        level0_dict = {'region1_T1_T2_T3_T4_to_S1_S2_S3_S4_S5_units': 100}

        # test that having too few underscore separated names in the key raises a ValueError
        with self.assertRaises(ValueError):
            deconstruct_dictionary(level0_dict)



if __name__ == '__main__':
    unittest.main()
