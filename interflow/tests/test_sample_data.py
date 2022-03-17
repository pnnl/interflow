import unittest
from interflow.sample_data import *
from interflow.reader import *


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

    def test_prep_water_use_2015(self):
        # test that, when run with no parameters, it just returns county list
        output = prep_water_use_2015()
        expected_columns = ['FIPS', 'State', 'County']
        output_columns = output.columns.to_list()
        self.assertEqual(output_columns, expected_columns)

        # test that there are 3,142 counties included
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

        # check that specifying a list of variables will return those variables
        output = prep_water_use_2015(variables=['FIPS', 'County', 'State', 'MI-WGWFr', 'MI-WGWSa', 'MI-WSWSa'])
        output_columns = output.columns.to_list()
        expected_columns = ['FIPS', 'County', 'State', 'MI-WGWFr', 'MI-WGWSa', 'MI-WSWSa']
        self.assertEqual(output_columns, expected_columns)

        # check that PR is not in output
        self.assertEqual("PR" in output['State'], False)

        # check that VI is not in output
        self.assertEqual("VI" in output['State'], False)

        # check that the required variables are included in the full output
        output = prep_water_use_2015(all_variables=True)
        output_columns = output.columns.to_list()
        expected_columns = ['FIPS', 'State', 'County', 'TP-TotPop',
                            'PS-WGWFr', 'PS-WSWFr', 'PS-WGWSa', 'PS-WSWSa',
                            'DO-PSDel', 'DO-WGWFr', 'DO-WSWFr',
                            'IN-WGWFr', 'IN-WSWFr', 'IN-WGWSa', 'IN-WSWSa',
                            'MI-WGWFr', 'MI-WSWFr', 'MI-WGWSa', 'MI-WSWSa',
                            'IC-WGWFr', 'IC-WSWFr', 'IC-RecWW',
                            'IG-WGWFr', 'IG-WSWFr', 'IG-RecWW',
                            'LI-WGWFr', 'LI-WSWFr',
                            'AQ-WGWFr', 'AQ-WGWSa', 'AQ-WSWFr', 'AQ-WSWSa',
                            'IR-WGWFr', 'IR-WSWFr', 'IR-RecWW', 'IG-CUsFr', 'IC-CUsFr',
                            'IR-CUsFr', 'PS-Wtotl', 'PT-WGWFr', 'PT-WGWSa', 'PT-WSWFr',
                            'PT-WSWSa', 'PT-RecWW', 'PT-PSDel']
        self.assertEqual(output_columns, expected_columns)

    def test_calc_irrigation_consumption(self):
        # test that the expected columns are returned
        output = calc_irrigation_consumption()

        output_columns = output.columns.to_list()
        expected_columns = ['FIPS', 'State', 'County',
                            'AGR_crop_fresh_surfacewater_withdrawal_mgd_to_CMP_total_total_total_total_mgd_fraction',
                            'AGR_crop_fresh_groundwater_withdrawal_mgd_to_CMP_total_total_total_total_mgd_fraction',
                            'AGR_crop_reclaimed_wastewater_import_mgd_to_CMP_total_total_total_total_mgd_fraction',
                            'AGR_golf_fresh_surfacewater_withdrawal_mgd_to_CMP_total_total_total_total_mgd_fraction',
                            'AGR_golf_fresh_groundwater_withdrawal_mgd_to_CMP_total_total_total_total_mgd_fraction',
                            'AGR_golf_reclaimed_wastewater_import_mgd_to_CMP_total_total_total_total_mgd_fraction',
                            'AGR_crop_ibt_total_import_mgd_to_CMP_total_total_total_total_mgd_fraction']
        self.assertEqual(output_columns, expected_columns)

        # test that there are 3,142 counties included
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

        # check that all of the fraction columns are between 0 and 1
        col_list = output.columns[3:].to_list()
        check_list = []
        for col in col_list:
            check_list.append(output[col].max() > 1)
            check_list.append(output[col].min() < 0)
        expected = "True" in check_list
        self.assertEqual(expected, False)

    def test_rename_water_data_2015(self):

        # get output
        output = rename_water_data_2015()

        # test that there are 3,142 counties included
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

        # test that, when run with no parameters, it just returns county list
        expected_columns = ['FIPS', 'State', 'County']
        output_columns = output.columns.to_list()
        self.assertEqual(output_columns, expected_columns)

        # check that specifying a list of variables will return those variables
        output = rename_water_data_2015(variables=['FIPS', 'County', 'State',
                                                'PWS_fresh_groundwater_withdrawal_total_mgd_from_WSW_fresh_groundwater_total_total_mgd'])
        output_columns = output.columns.to_list()
        expected_columns = ['FIPS', 'County', 'State',
                            'PWS_fresh_groundwater_withdrawal_total_mgd_from_WSW_fresh_groundwater_total_total_mgd']
        self.assertEqual(output_columns, expected_columns)

    def test_calc_population_county_weight(self):

        # prepare test data
        df = get_electricity_demand_data()
        df = df[df.Year == 2015]
        df = df[df.State != 'US']
        df = df.loc[df['Industry Sector Category'] == 'Total Electric Industry']

        # get output
        output = calc_population_county_weight(df)

        # test that there are 3,242 counties in output
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

        # test that the pop_weight column only includes values less than or equal to 1
        x = output['pop_weight'].max() > 1
        self.assertEqual(x, False)

        # test that the pop_weight column only includes values greater than or equal to 0
        x = output['pop_weight'].min() < 0
        self.assertEqual(x, False)

        # test that the sum of population weights in each state are equal to 1
        output_state = output.groupby("State", as_index=False).sum()
        state_percent = output_state['pop_weight'].mean()
        self.assertEqual(state_percent, 1)

        # test that there are 51 states accounted for
        output_state = output.groupby("State", as_index=False).sum()
        state_count = output_state['pop_weight'].count()
        self.assertEqual(state_count, 51)

        # test that the county percentages are being correctly calculated
        df = get_electricity_demand_data()
        df = df[df.Year == 2015]
        df = df[df.State != 'US']
        df = df.loc[df['Industry Sector Category'] == 'Total Electric Industry']
        out = calc_population_county_weight(df)
        out = out[out.State == 'AL']
        x = out['pop_weight'].to_list()
        output = x[0]

        df_county = rename_water_data_2015(variables=['FIPS', 'State', 'County', 'population'])
        county_pop = df_county['population'][0]
        df_state = df_county.groupby("State", as_index=False).sum()
        s = df_state[df_state.State == 'AL']
        state_pop = s['population'][1]
        expected = county_pop / state_pop
        self.assertEqual(output, expected)

    def test_prep_water_use_1995(self):

        # load data
        output = prep_water_use_1995()

        # test that, when run with no parameters, it just returns county list
        output = prep_water_use_2015()
        expected_columns = ['FIPS', 'State', 'County']
        output_columns = output.columns.to_list()
        self.assertEqual(output_columns, expected_columns)

        # test that there are 3,142 counties included
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

        # check that specifying a list of variables will return those variables
        output = prep_water_use_1995(variables=['FIPS', 'PS-GWPop'])
        output_columns = output.columns.to_list()
        expected_columns = ['FIPS', 'PS-GWPop']
        self.assertEqual(output_columns, expected_columns)

        # check that PR is not in output
        self.assertEqual("PR" in output['State'], False)

        # check that VI is not in output
        self.assertEqual("VI" in output['State'], False)




if __name__ == '__main__':
    unittest.main()
