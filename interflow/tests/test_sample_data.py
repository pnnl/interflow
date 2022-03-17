import unittest
from interflow.sample_data import *
from interflow.reader import *


class MyTestCase(unittest.TestCase):
    """Conduct tests for functions of sample_data.py."""

    def test_convert_kwh_bbtu(self):
        # test_interflow that the outcome is as expected
        output = convert_kwh_bbtu(500)
        expected = 0.00170607

        self.assertEqual(output, expected)

    def test_convert_mwh_bbtu(self):
        # test_interflow that the outcome is as expected
        output = convert_mwh_bbtu(500)
        expected = 1.706

        self.assertEqual(output, expected)

    def test_prep_water_use_2015(self):
        # test_interflow that, when run with no parameters, it just returns county list
        output = prep_water_use_2015()
        expected_columns = ['FIPS', 'State', 'County']
        output_columns = output.columns.to_list()
        self.assertEqual(output_columns, expected_columns)

        # test_interflow that there are 3,142 counties included
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
        # test_interflow that the expected columns are returned
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

        # test_interflow that there are 3,142 counties included
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

        # test_interflow that there are 3,142 counties included
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

        # test_interflow that, when run with no parameters, it just returns county list
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

        # prepare test_interflow data
        df = get_electricity_demand_data()
        df = df[df.Year == 2015]
        df = df[df.State != 'US']
        df = df.loc[df['Industry Sector Category'] == 'Total Electric Industry']

        # get output
        output = calc_population_county_weight(df)

        # test_interflow that there are 3,242 counties in output
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

        # test_interflow that the pop_weight column only includes values less than or equal to 1
        x = output['pop_weight'].max() > 1
        self.assertEqual(x, False)

        # test_interflow that the pop_weight column only includes values greater than or equal to 0
        x = output['pop_weight'].min() < 0
        self.assertEqual(x, False)

        # test_interflow that the sum of population weights in each state are equal to 1
        output_state = output.groupby("State", as_index=False).sum()
        state_percent = output_state['pop_weight'].mean()
        self.assertEqual(state_percent, 1)

        # test_interflow that there are 51 states accounted for
        output_state = output.groupby("State", as_index=False).sum()
        state_count = output_state['pop_weight'].count()
        self.assertEqual(state_count, 51)

        # test_interflow that the county percentages are being correctly calculated
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

        # test_interflow that, when run with no parameters, it just returns county list
        output = prep_water_use_2015()
        expected_columns = ['FIPS', 'State', 'County']
        output_columns = output.columns.to_list()
        self.assertEqual(output_columns, expected_columns)

        # test_interflow that there are 3,142 counties included
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

        # check that specifying a list of variables will return those variables
        output = prep_water_use_1995(variables=['FIPS', 'PS-GWPop'])
        output_columns = output.columns.to_list()
        expected_columns = ['FIPS', 'PS-GWPop']
        self.assertEqual(output_columns, expected_columns)

        # check that PR is not in output
        output = prep_water_use_1995(variables=['FIPS', 'State'])
        self.assertEqual("PR" in output['State'], False)

        # check that VI is not in output
        self.assertEqual("VI" in output['State'], False)

        # check that removed FIPS are not in FIPS column
        removed_fips = ["02232", "02280", "12025", "46113", "02270",
                        "02201"]
        check_list = []
        for fips in removed_fips:
            check_list.append(fips in output['FIPS'])
        expected = "True" in check_list

        self.assertEqual(expected, False)

        # check that added FIPS are in FIPS column
        removed_fips = ["02105", "02195", "12086", "46102", "02158",
                        "02198", "02230","02195", "08013"]
        check_list = []
        for fips in removed_fips:
            check_list.append(fips in output['FIPS'])
        expected = "False" in check_list
        self.assertEqual(expected, False)

        # check that all FIPS are unique
        self.assertTrue(output["FIPS"].is_unique)

    def test_calc_irrigation_conveyance_loss_fraction(self):

        # read in data
        output = calc_irrigation_conveyance_loss_fraction(loss_cap=True, loss_cap_amt=.8)

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

        # check that all of the fraction columns are between 0 and the loss cap
        loss_cap_amt = .8
        col_list = output.columns[3:].to_list()
        check_list = []
        for col in col_list:
            check_list.append(output[col].max() > loss_cap_amt)
            check_list.append(output[col].min() < 0)
        expected = "True" in check_list
        self.assertEqual(expected, False)

    def test_calc_irrigation_discharge_flows(self):

        # collect output
        output = calc_irrigation_discharge_flows()

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

        # check that all of the fraction columns are between 0 and the loss cap
        col_list = output.columns[3:].to_list()
        check_list = []
        for col in col_list:
            check_list.append(output[col].max() > 1)
            check_list.append(output[col].min() < 0)
        expected = "True" in check_list
        self.assertEqual(expected, False)

    def test_prep_consumption_fraction(self):

        # collect output
        output = calc_irrigation_discharge_flows()

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

        # check that all of the fraction columns are between 0 and the loss cap
        col_list = output.columns[3:].to_list()
        check_list = []
        for col in col_list:
            check_list.append(output[col].max() > 1)
            check_list.append(output[col].min() < 0)
        expected = "True" in check_list
        self.assertEqual(expected, False)

        # make sure there are no blank values
        is_NaN = output.isnull()
        row_has_NaN = is_NaN.any(axis=1)
        rows_with_NaN = output[row_has_NaN]
        result = len(rows_with_NaN)
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()