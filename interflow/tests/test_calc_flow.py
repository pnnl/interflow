import unittest
import numpy as np
from interflow.calc_flow import *


class TestCalcFlow(unittest.TestCase):
    """Conduct tests for functions of calc_flow.py."""

    def test_calc_flow(self):
        # create sample test data
        sample_data = read_sample_data()
        first_region = sample_data[sample_data.columns[0]].iloc[0]
        first_column = sample_data.columns[0]
        sample_data = sample_data.loc[sample_data[first_column] == first_region]

        # check that providing an incorrect level number leads to a ValueError
        with self.assertRaises(ValueError):
            calculate(data=sample_data, level=7)

        # check that providing a dataframe with the incorrect number of columns raises a ValueError
        sample_extra_column = sample_data.copy()
        sample_extra_column['extra'] = 1
        with self.assertRaises(ValueError):
            calculate(data=sample_extra_column, level=5)

        # check that providing a region name that isn't in the dataframe returns a ValueError
        with self.assertRaises(ValueError):
            calculate(data=sample_data, level=5, region_name='99999')

        # check that the level5 output dataframe is at the correct level of granularity
        df = calculate(data=sample_data, level=5)
        output = len(df.columns)
        expected = 13
        self.assertEqual(output, expected)

        # check that the level4 output dataframe is at the correct level of granularity
        df = calculate(data=sample_data, level=4)
        output = len(df.columns)
        expected = 11
        self.assertEqual(output, expected)

        # check that the level3 output dataframe is at the correct level of granularity
        df = calculate(data=sample_data, level=3)
        output = len(df.columns)
        expected = 9
        self.assertEqual(output, expected)

        # check that the level2 output dataframe is at the correct level of granularity
        df = calculate(data=sample_data, level=2)
        output = len(df.columns)
        expected = 7
        self.assertEqual(output, expected)

        # check that the level1 output dataframe is at the correct level of granularity
        df = calculate(data=sample_data, level=1)
        output = len(df.columns)
        expected = 5
        self.assertEqual(output, expected)

        # create a sample input dataframe to test calculations
        inputs = [['01', 'A_collect', 'A1w', 'A2w', 'A3w', 'A4w', 'A5w', 'Aunit', 'B1', 'B2', 'B3', 'B4', 'B5', 'Bunit',
                 'flow_value', 10],
                ['01', 'B_calculate', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'A1w', 'A2w', 'A3w', 'A4w', 'A5w',
                 'Aunit', 'intensity', 2],
                ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'C1e', 'C2e', 'C3e', 'C4e', 'C5e',
                 'CeUnit', 'fraction', .25],
                ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'D1e', 'D2e', 'D3e', 'D4e', 'D5e',
                 'DeUnit', 'fraction', .75],
                ['01', 'D_discharge', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'E1e', 'E2e', 'E3e', 'E4e', 'E5e',
                 'EeUnit', 'fraction', .20],
                ['01', 'D_discharge', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'F1e', 'F2e', 'F3e', 'F4e', 'F5e',
                 'FeUnit', 'fraction', .8]]
        data = pd.DataFrame(inputs, columns=['region', 'type', 't1', 't2', 't3', 't4', 't5', 'T_unit',
                                             's1', 's2', 's3', 's4', 's5', 'S_unit', 'parameter', 'value'])

        # calculate output
        df = calculate(data=data, level=5)

        # test that the first value returned is calculated correctly
        self.assertEqual(df.iloc[0]['value'], 10)

        # test that the source flows returned are calculated correctly
        self.assertEqual(df.iloc[1]['value'], 5)

        # test that the source flows returned are calculated correctly
        self.assertEqual(df.iloc[2]['value'], 15)

        # test that the source flows returned are calculated correctly
        self.assertEqual(df.iloc[3]['value'], 4)

        # test that the source flows returned are calculated correctly
        self.assertEqual(df.iloc[4]['value'], 16)

        # create data to test sum of level 2 differentiation for source fractions (i.e., same major sector)
        inputs = [['01', 'A_collect', 'A1w', 'A2w', 'A3w', 'A4w', 'A5w', 'Aunit','B1', 'B2', 'B3', 'B4', 'B5',
                            'Bunit', 'flow_value', 10],
        ['01', 'B_calculate', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit','A1w', 'A2w', 'A3w', 'A4w', 'A5w', 'Aunit',
         'intensity', 2],
        ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit','C1e', 'Ca2e', 'Ca3e', 'Ca4e', 'Ca5e', 'CeUnit',
         'fraction', .20],
        ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit','C1e', 'Cb2e', 'Cb3e', 'Cb4e', 'Cb5e', 'CeUnit',
         'fraction', .05],
        ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit','D1e', 'D2e', 'D3e', 'D4e', 'D5e', 'DeUnit',
         'fraction', .75],
        ['01', 'D_discharge', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit','E1e', 'E2e', 'E3e', 'E4e', 'E5e', 'EeUnit',
         'fraction', .20],
        ['01', 'D_discharge', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit','F1e', 'F2e', 'F3e', 'F4e', 'F5e', 'FeUnit',
         'fraction', .8]]

        data = pd.DataFrame(inputs, columns=['region', 'type', 't1', 't2', 't3', 't4', 't5', 'T_unit',
                                             's1', 's2', 's3', 's4', 's5', 'S_unit', 'parameter', 'value'])

        # calculate output
        df5 = calculate(data=data, level=5)

        # test that the second value where the split occurs is calculated correctly
        self.assertEqual(df5.iloc[1]['value'], 4)
        self.assertEqual(df5.iloc[2]['value'], 1)

        # create data to test sum of level 3 differentiation for source fractions
        inputs = [['01', 'A_collect', 'A1w', 'A2w', 'A3w', 'A4w', 'A5w', 'Aunit','B1', 'B2', 'B3', 'B4', 'B5',
                            'Bunit', 'flow_value', 10],
        ['01', 'B_calculate', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit','A1w', 'A2w', 'A3w', 'A4w', 'A5w', 'Aunit',
         'intensity', 2],
        ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit','C1e', 'C2e', 'Ca3e', 'Ca4e', 'Ca5e', 'CeUnit',
         'fraction', .10],
        ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit','C1e', 'C2e', 'Cb3e', 'Cb4e', 'Cb5e', 'CeUnit',
         'fraction', .15],
        ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit','D1e', 'D2e', 'D3e', 'D4e', 'D5e', 'DeUnit',
         'fraction', .75],
        ['01', 'D_discharge', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit','E1e', 'E2e', 'E3e', 'E4e', 'E5e', 'EeUnit',
         'fraction', .20],
        ['01', 'D_discharge', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit','F1e', 'F2e', 'F3e', 'F4e', 'F5e', 'FeUnit',
         'fraction', .8]]

        data = pd.DataFrame(inputs, columns=['region', 'type', 't1', 't2', 't3', 't4', 't5', 'T_unit',
                                             's1', 's2', 's3', 's4', 's5', 'S_unit', 'parameter', 'value'])

        # calculate output
        df5 = calculate(data=data, level=5)

        # test that the third value where the split occurs is calculated correctly
        self.assertEqual(df5.iloc[1]['value'], 2)
        self.assertEqual(df5.iloc[2]['value'], 3)

        # create data to test sum of level 4 differentiation for source fractions
        inputs = [['01', 'A_collect', 'A1w', 'A2w', 'A3w', 'A4w', 'A5w', 'Aunit','B1', 'B2', 'B3', 'B4', 'B5',
                            'Bunit', 'flow_value', 10],
        ['01', 'B_calculate', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit','A1w', 'A2w', 'A3w', 'A4w', 'A5w', 'Aunit',
         'intensity', 2],
        ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit','C1e', 'C2e', 'C3e', 'Ca4e', 'Ca5e', 'CeUnit',
         'fraction', .22],
        ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit','C1e', 'C2e', 'C3e', 'Cb4e', 'Cb5e', 'CeUnit',
         'fraction', .03],
        ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit','D1e', 'D2e', 'D3e', 'D4e', 'D5e', 'DeUnit',
         'fraction', .75],
        ['01', 'D_discharge', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit','E1e', 'E2e', 'E3e', 'E4e', 'E5e', 'EeUnit',
         'fraction', .20],
        ['01', 'D_discharge', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit','F1e', 'F2e', 'F3e', 'F4e', 'F5e', 'FeUnit',
         'fraction', .8]]

        data = pd.DataFrame(inputs, columns=['region', 'type', 't1', 't2', 't3', 't4', 't5', 'T_unit',
                                             's1', 's2', 's3', 's4', 's5', 'S_unit', 'parameter', 'value'])

        # calculate output
        df5 = calculate(data=data, level=5)

        # test that the third value where the split occurs is calculated correctly
        self.assertEqual(df5.iloc[1]['value'], 4.4)
        self.assertEqual(df5.iloc[2]['value'], 0.6)

        # create data to test sum of level 5 differentiation for source fractions
        inputs = [['01', 'A_collect', 'A1w', 'A2w', 'A3w', 'A4w', 'A5w', 'Aunit','B1', 'B2', 'B3', 'B4', 'B5',
                            'Bunit', 'flow_value', 10],
        ['01', 'B_calculate', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit','A1w', 'A2w', 'A3w', 'A4w', 'A5w', 'Aunit',
         'intensity', 2],
        ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit','C1e', 'C2e', 'C3e', 'C4e', 'Ca5e', 'CeUnit',
         'fraction', .01],
        ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit','C1e', 'C2e', 'C3e', 'C4e', 'Cb5e', 'CeUnit',
         'fraction', .24],
        ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit','D1e', 'D2e', 'D3e', 'D4e', 'D5e', 'DeUnit',
         'fraction', .75],
        ['01', 'D_discharge', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit','E1e', 'E2e', 'E3e', 'E4e', 'E5e', 'EeUnit',
         'fraction', .20],
        ['01', 'D_discharge', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit','F1e', 'F2e', 'F3e', 'F4e', 'F5e', 'FeUnit',
         'fraction', .8]]

        data = pd.DataFrame(inputs, columns=['region', 'type', 't1', 't2', 't3', 't4', 't5', 'T_unit',
                                             's1', 's2', 's3', 's4', 's5', 'S_unit', 'parameter', 'value'])

        # calculate output
        df5 = calculate(data=data, level=5)

        # test that the fourth value where the split occurs is calculated correctly
        self.assertEqual(df5.iloc[1]['value'], .2)
        self.assertEqual(df5.iloc[2]['value'], 4.8)

        # create data to test sum of level 2 differentiation for discharge fractions
        inputs = [['01', 'A_collect', 'A1w', 'A2w', 'A3w', 'A4w', 'A5w', 'Aunit', 'B1', 'B2', 'B3', 'B4', 'B5',
                   'Bunit', 'flow_value', 10],
                  ['01', 'B_calculate', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'A1w', 'A2w', 'A3w', 'A4w', 'A5w',
                   'Aunit',
                   'intensity', 2],
                  ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'C1e', 'Ca2e', 'Ca3e', 'Ca4e', 'Ca5e',
                   'CeUnit',
                   'fraction', .20],
                  ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'C1e', 'Cb2e', 'Cb3e', 'Cb4e', 'Cb5e',
                   'CeUnit',
                   'fraction', .05],
                  ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'D1e', 'D2e', 'D3e', 'D4e', 'D5e',
                   'DeUnit',
                   'fraction', .75],
                  ['01', 'D_discharge', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'E1e', 'E2e', 'E3e', 'E4e', 'E5e',
                   'EeUnit',
                   'fraction', .20],
                  ['01', 'D_discharge', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'E1e', 'F2e', 'F3e', 'F4e', 'F5e',
                   'FeUnit',
                   'fraction', .30],
                  ['01', 'D_discharge', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'G1e', 'G2e', 'G3e', 'G4e', 'G5e',
                   'GeUnit',
                   'fraction', .5]
                  ]

        data = pd.DataFrame(inputs, columns=['region', 'type', 't1', 't2', 't3', 't4', 't5', 'T_unit',
                                             's1', 's2', 's3', 's4', 's5', 'S_unit', 'parameter', 'value'])

        # calculate output
        df5 = calculate(data=data, level=5)

        # test that the second value where the split occurs is calculated correctly
        self.assertEqual(df5.iloc[4]['value'], 4)
        self.assertEqual(df5.iloc[5]['value'], 6)

        # create data to test sum of level 3 differentiation for discharge fractions\
        inputs = [['01', 'A_collect', 'A1w', 'A2w', 'A3w', 'A4w', 'A5w', 'Aunit', 'B1', 'B2', 'B3', 'B4', 'B5',
                   'Bunit', 'flow_value', 10],
                  ['01', 'B_calculate', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'A1w', 'A2w', 'A3w', 'A4w', 'A5w',
                   'Aunit',
                   'intensity', 2],
                  ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'C1e', 'Ca2e', 'Ca3e', 'Ca4e', 'Ca5e',
                   'CeUnit',
                   'fraction', .20],
                  ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'C1e', 'Cb2e', 'Cb3e', 'Cb4e', 'Cb5e',
                   'CeUnit',
                   'fraction', .05],
                  ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'D1e', 'D2e', 'D3e', 'D4e', 'D5e',
                   'DeUnit',
                   'fraction', .75],
                  ['01', 'D_discharge', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'E1e', 'E2e', 'E3e', 'E4e', 'E5e',
                   'EeUnit',
                   'fraction', .25],
                  ['01', 'D_discharge', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'E1e', 'E2e', 'F3e', 'F4e', 'F5e',
                   'FeUnit',
                   'fraction', .25],
                  ['01', 'D_discharge', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'G1e', 'G2e', 'G3e', 'G4e', 'G5e',
                   'GeUnit',
                   'fraction', .5]
                  ]

        data = pd.DataFrame(inputs, columns=['region', 'type', 't1', 't2', 't3', 't4', 't5', 'T_unit',
                                             's1', 's2', 's3', 's4', 's5', 'S_unit', 'parameter', 'value'])

        # calculate output
        df5 = calculate(data=data, level=5)

        # test that the value where the split occurs is calculated correctly
        self.assertEqual(df5.iloc[4]['value'], 5)
        self.assertEqual(df5.iloc[5]['value'], 5)

        # create data to test sum of level 4 differentiation for discharge fractions\
        inputs = [['01', 'A_collect', 'A1w', 'A2w', 'A3w', 'A4w', 'A5w', 'Aunit', 'B1', 'B2', 'B3', 'B4', 'B5',
                   'Bunit', 'flow_value', 10],
                  ['01', 'B_calculate', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'A1w', 'A2w', 'A3w', 'A4w', 'A5w',
                   'Aunit',
                   'intensity', 2],
                  ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'C1e', 'Ca2e', 'Ca3e', 'Ca4e', 'Ca5e',
                   'CeUnit',
                   'fraction', .20],
                  ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'C1e', 'Cb2e', 'Cb3e', 'Cb4e', 'Cb5e',
                   'CeUnit',
                   'fraction', .05],
                  ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'D1e', 'D2e', 'D3e', 'D4e', 'D5e',
                   'DeUnit',
                   'fraction', .75],
                  ['01', 'D_discharge', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'E1e', 'E2e', 'E3e', 'E4e', 'E5e',
                   'EeUnit',
                   'fraction', .02],
                  ['01', 'D_discharge', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'E1e', 'E2e', 'E3e', 'F4e', 'F5e',
                   'FeUnit',
                   'fraction', .48],
                  ['01', 'D_discharge', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'G1e', 'G2e', 'G3e', 'G4e', 'G5e',
                   'GeUnit',
                   'fraction', .5]
                  ]

        data = pd.DataFrame(inputs, columns=['region', 'type', 't1', 't2', 't3', 't4', 't5', 'T_unit',
                                             's1', 's2', 's3', 's4', 's5', 'S_unit', 'parameter', 'value'])

        # calculate output
        df5 = calculate(data=data, level=5)

        # test that the third value where the split occurs is calculated correctly
        self.assertEqual(df5.iloc[4]['value'], .4)
        self.assertEqual(df5.iloc[5]['value'], 9.6)

        # create data to test sum of level 5 differentiation for discharge fractions\
        inputs = [['01', 'A_collect', 'A1w', 'A2w', 'A3w', 'A4w', 'A5w', 'Aunit', 'B1', 'B2', 'B3', 'B4', 'B5',
                   'Bunit', 'flow_value', 10],
                  ['01', 'B_calculate', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'A1w', 'A2w', 'A3w', 'A4w', 'A5w',
                   'Aunit',
                   'intensity', 2],
                  ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'C1e', 'Ca2e', 'Ca3e', 'Ca4e', 'Ca5e',
                   'CeUnit',
                   'fraction', .20],
                  ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'C1e', 'Cb2e', 'Cb3e', 'Cb4e', 'Cb5e',
                   'CeUnit',
                   'fraction', .05],
                  ['01', 'C_source', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'D1e', 'D2e', 'D3e', 'D4e', 'D5e',
                   'DeUnit',
                   'fraction', .75],
                  ['01', 'D_discharge', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'E1e', 'E2e', 'E3e', 'E4e', 'E5e',
                   'EeUnit',
                   'fraction', .2],
                  ['01', 'D_discharge', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'E1e', 'E2e', 'E3e', 'E4e', 'F5e',
                   'FeUnit',
                   'fraction', .3],
                  ['01', 'D_discharge', 'A1e', 'A2e', 'A3e', 'A4e', 'A5e', 'AeUnit', 'G1e', 'G2e', 'G3e', 'G4e', 'G5e',
                   'GeUnit',
                   'fraction', .5]
                  ]

        data = pd.DataFrame(inputs, columns=['region', 'type', 't1', 't2', 't3', 't4', 't5', 'T_unit',
                                             's1', 's2', 's3', 's4', 's5', 'S_unit', 'parameter', 'value'])

        # calculate output
        df5 = calculate(data=data, level=5)

        # test that the value where the split occurs is calculated correctly
        self.assertEqual(df5.iloc[4]['value'], 4)
        self.assertEqual(df5.iloc[5]['value'], 6)

        # create data to test that multiple regions give distinct values
        inputs = [['01', 'A_collect', 'A1w', 'A2w', 'A3w', 'A4w', 'A5w', 'Aunit', 'B1', 'B2', 'B3', 'B4', 'B5',
                   'Bunit', 'flow_value', 10],
                  ['02', 'A_collect', 'A1w', 'A2w', 'A3w', 'A4w', 'A5w', 'Aunit', 'B1', 'B2', 'B3', 'B4', 'B5',
                   'Bunit', 'flow_value', 50]]

        data = pd.DataFrame(inputs, columns=['region', 'type', 't1', 't2', 't3', 't4', 't5', 'T_unit',
                                             's1', 's2', 's3', 's4', 's5', 'S_unit', 'parameter', 'value'])

        # calculate output
        df5 = calculate(data=data, level=5)

        # test that the value where the split occurs is calculated correctly
        self.assertEqual(df5.iloc[0]['value'], 10)
        self.assertEqual(df5.iloc[1]['value'], 50)


if __name__ == '__main__':
    unittest.main()
