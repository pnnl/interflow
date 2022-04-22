import unittest
from interflow.analyze import *
from interflow.calc_flow import *


class TestAnalyze(unittest.TestCase):
    def test_group_results(self):
        """Test group_results()."""

        # load output data for a single region
        data = read_sample_data()
        region = '01001'
        df_in = calculate(data=data, region_name=region, level=5)

        # returns a dataframe
        output = group_results(df=df_in, output_level=1)
        self.assertTrue(type(output) == pd.DataFrame)

        # check that grouping results to level 1 gives 5 columns
        output = group_results(df=df_in, output_level=1)
        x = len(output.columns.to_list())
        self.assertTrue(x == 5)

        # check that grouping results to level 2 gives 7 columns
        output = group_results(df=df_in, output_level=2)
        x = len(output.columns.to_list())
        self.assertTrue(x == 7)

        # check that grouping results to level 3 gives 9 columns
        output = group_results(df=df_in, output_level=3)
        x = len(output.columns.to_list())
        self.assertTrue(x == 9)

        # check that grouping results to level 4 gives 11 columns
        output = group_results(df=df_in, output_level=4)
        x = len(output.columns.to_list())
        self.assertTrue(x == 11)

        # check that grouping results to level 5 gives 13 columns
        output = group_results(df=df_in, output_level=5)
        x = len(output.columns.to_list())
        self.assertTrue(x == 13)

        # check that the sum of level 5 flows to the same node add to the level 1 output
        output_level1 = group_results(df=df_in, output_level=1)
        output_level1 = output_level1[output_level1.T1 == 'CMP']
        output_level1 = output_level1[output_level1.S1 == 'AGR']
        x_1 = output_level1['value'].sum()

        output_level5 = group_results(df=df_in, output_level=5)
        output_level5 = output_level5[output_level5.T1 == 'CMP']
        output_level5 = output_level5[output_level5.S1 == 'AGR']
        x_5 = output_level5['value'].sum()

        self.assertEqual(x_1, x_5)

        # check that the sum of level 4 flows to the same node add to the level 1 output
        output_level4 = group_results(df=df_in, output_level=4)
        output_level4 = output_level4[output_level4.T1 == 'CMP']
        output_level4 = output_level4[output_level4.S1 == 'AGR']
        x_4 = output_level4['value'].sum()

        self.assertEqual(x_1, x_4)

        # check that the sum of level 3 flows to the same node add to the level 1 output
        output_level3 = group_results(df=df_in, output_level=3)
        output_level3 = output_level3[output_level3.T1 == 'CMP']
        output_level3 = output_level3[output_level3.S1 == 'AGR']
        x_3 = output_level3['value'].sum()

        self.assertEqual(x_1, x_3)

        # check that the sum of level 2 flows to the same node add to the level 1 output
        output_level2 = group_results(df=df_in, output_level=2)
        output_level2 = output_level2[output_level2.T1 == 'CMP']
        output_level2 = output_level2[output_level2.S1 == 'AGR']
        x_2 = output_level2['value'].sum()

        self.assertEqual(x_1, x_2)

if __name__ == '__main__':
    unittest.main()
