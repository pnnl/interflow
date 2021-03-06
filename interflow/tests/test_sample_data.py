import unittest
from interflow.sample_data import *
from interflow.reader import *


class TestSampleData(unittest.TestCase):
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
                            'AGR_golf_reclaimed_wastewater_import_mgd_to_CMP_total_total_total_total_mgd_fraction'
                            ]
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

        # test  that the sum of population weights in each state are equal to 1
        output_state = output.groupby("State", as_index=False).sum()
        state_percent = output_state['pop_weight'].mean()
        self.assertEqual(state_percent, 1)

        # test  that there are 51 states accounted for
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
                        "02198", "02230", "02195", "08013"]
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

    def test_prep_public_water_supply_fraction(self):

        # collect output
        output = prep_public_water_supply_fraction()

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
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that fraction calculations are computing correctly for commercial
        fips = '56037'
        result = output[output.FIPS == fips]
        result = result['com_pws_fraction'].iloc[0]

        input_df = prep_water_use_1995(variables=['FIPS', 'State', 'PS-DelDO',
                                                  'PS-DelPT', 'PS-DelCO', 'PS-DelIN'])
        input_df = input_df[input_df.FIPS == fips]
        input_df['out'] = input_df['PS-DelCO'] / input_df['PS-DelDO'] + input_df['PS-DelPT']
        expected = input_df['out'].iloc[0]

        # check that fraction calculations are computing correctly for industrial
        fips = '56037'
        result = output[output.FIPS == fips]
        result = result['ind_pws_fraction'].iloc[0]

        input_df = prep_water_use_1995(variables=['FIPS', 'State', 'PS-DelDO',
                                                  'PS-DelPT', 'PS-DelCO', 'PS-DelIN'])
        input_df = input_df[input_df.FIPS == fips]
        input_df['out'] = input_df['PS-DelIN'] / input_df['PS-DelDO'] + input_df['PS-DelPT']
        expected = input_df['out'].iloc[0]

        self.assertEqual(result, expected)

    def test_calc_pws_commercial_industrial_flows(self):

        # get output
        output = calc_pws_commercial_industrial_flows()

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

    def test_calc_discharge_fractions(self):

        # collect output
        output = calc_discharge_fractions()

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
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

    def test_prep_irrigation_pws_ratio(self):

        # collect output
        output = prep_irrigation_pws_ratio()

        # check that there are the correct number of counties
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

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

    def test_prep_interbasin_transfer_data(self):

        # collect output
        output = prep_interbasin_transfer_data()

        # check that all FIPS are unique
        self.assertTrue(output["FIPS"].is_unique)

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

        # check that dropped variables are not in output
        drop_list = ['ibt_energy_intensity_bbtu', 'water_interbasin_mgd', 'pws_ibt_pct', 'irrigation_ibt_pct']
        check_list = []
        for item in drop_list:
            check_list.append(item in output.columns)
        self.assertFalse(True in check_list)

    def test_prep_pws_to_pwd(self):
        # collect output
        output = prep_pws_to_pwd()

        # check that all FIPS are unique
        self.assertTrue(output["FIPS"].is_unique)

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

    def test_prep_county_identifier(self):

        # collect output
        output = prep_pws_to_pwd()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

    def test_prep_wastewater_data(self):

        # collect output
        output = prep_wastewater_data()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

    def test_calc_sc_ww_values(self):

        # collect output
        output = calc_sc_ww_values()

        # make sure only south carolina is included
        output_state = output.groupby("State", as_index=False).sum()
        self.assertEqual(1, len(output_state))

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that dropped variables are not in output
        drop_list = ['total_municipal', 'advanced_municipal', 'secondary_municipal']
        check_list = []
        for item in drop_list:
            check_list.append(item in output.columns)
        self.assertFalse(True in check_list)

    def test_combine_ww_data(self):

        # collect output
        output = calc_sc_ww_values()

        # make sure only south carolina is included
        output_state = output.groupby("State", as_index=False).sum()
        self.assertEqual(1, len(output_state))

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

    def test_prep_power_plant_location(self):

        # collect output
        output = prep_power_plant_location()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that the fixed cities are not in data
        city_list = ['VAchesapeakecity', 'VAportsmouthcity', 'VAhopewellcity', 'VAalexandriacity',
                     'VAcovingtoncity', 'VAsuffolkcity', 'VAharrisonburgcity', 'VAsalemcity',
                     'VAlynchburgcity', 'VAdanvillecity', 'VAmanassascity', 'VAhamptoncity',
                     'VAvirginiabeachcity', 'VAbristolcity', 'MOstlouiscity']

        check_list = []
        for item in city_list:
            check_list.append(item in output['county_identifier'].to_list())
        self.assertFalse(True in check_list)

    def test_prep_electricity_fuel(self):

        # collect output
        output = prep_electricity_fuel()

        # check that plant code 99999 is not in dataset
        self.assertFalse(99999 in output['plant_code'].to_list())

        # check that pumped storage is not in the dataset
        self.assertFalse('pumpedstorage' in output['prime_mover'].to_list())

        # check that required columns are in output
        column_list = ['plant_code', 'fuel_type', 'prime_mover', 'fuel_amt',
                       'water_withdrawal_mgd', 'water_consumption_mgd',
                       'withdrawal_pct', 'consumption_pct', 'generation_bbtu', 'FIPS']
        self.assertEqual(column_list, output.columns.to_list())

    def test_prep_electricity_cooling(self):

        # collect output
        output = prep_electricity_cooling()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        column_list = ['plant_code', 'fuel_type', 'prime_mover', 'fuel_amt', 'generation_bbtu', 'FIPS',
                       'COOLING_TYPE', 'WATER_SOURCE_CODE', 'WATER_TYPE_CODE', 'WITHDRAWAL', 'CONSUMPTION',
                       'SURFACE_DISCHARGE_MGD', 'OCEAN_DISCHARGE_MGD']

        self.assertEqual(column_list, output.columns.to_list())

        # check to make sure that power plant types with no cooling have zero cooling
        result = output.loc[output['fuel_type'] == 'hydro']['WITHDRAWAL'].mean()
        self.assertEqual(result, 0)
        result = output.loc[output['fuel_type'] == 'wind']['WITHDRAWAL'].mean()
        self.assertEqual(result, 0)
        result = output.loc[output['fuel_type'] == 'solar']['WITHDRAWAL'].mean()
        self.assertEqual(result, 0)
        result = output.loc[output['fuel_type'] == 'geothermal']['WITHDRAWAL'].mean()
        self.assertEqual(result, 0)

        # check that withdrawals are equal to discharges
        result = output['WITHDRAWAL'].sum() - \
                 (output['CONSUMPTION'].sum() + output['SURFACE_DISCHARGE_MGD'].sum()
                  + output['OCEAN_DISCHARGE_MGD'].sum())
        self.assertEqual(result, 0)

    def test_prep_generation_fuel_flows(self):
        # collect output
        output = prep_generation_fuel_flows()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

        # check that the discharge fractions are between 0 and 1
        col_list = output.columns[76:].to_list()
        check_list = []
        for col in col_list:
            check_list.append(output[col].max() > 1)
            check_list.append(output[col].min() < 0)
        expected = "True" in check_list
        self.assertEqual(expected, False)

    def test_prep_electricity_cooling_flows(self):

        # collect output
        output = prep_electricity_cooling_flows()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

    def test_calc_hydro_water_intensity(self):

        # collect output
        output = calc_hydro_water_intensity()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

        # check that all of the fraction columns are between 0 and the intensity cap
        loss_cap_amt = 6000000
        column = output.columns[3]
        max_val = output[column].max() > loss_cap_amt
        self.assertFalse(max_val)

        min_val = output[column].min() < 0
        self.assertFalse(min_val)

        # check that all of the fraction columns are between 0 and a
        loss_cap_amt = 6000000
        column = output.columns[3]
        max_val = output[column].max() > loss_cap_amt
        self.assertFalse(max_val)

        min_val = output[column].min() < 0
        self.assertFalse(min_val)

    def test_prep_pumping_energy_fuel_data(self):

        # collect output
        output = prep_pumping_energy_fuel_data()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that there are the correct number of counties
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

    def test_prep_pumping_intensity_data(self):

        # collect output
        output = prep_pumping_energy_fuel_data()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

    def test_prep_pws_treatment_dist_intensity_values(self):

        # collect output
        output = prep_pws_treatment_dist_intensity_values()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

        # test that the correct intensity values are assigned to the correct variables
        fgw_treat = 'PWS_treatment_fresh_groundwater_total_bbtu_from_PWS_fresh_groundwater_withdrawal_total_mgd_intensity'
        expected = convert_kwh_bbtu(205)
        x = output[fgw_treat].mean()
        self.assertAlmostEqual(x, expected, 10)

        fsw_treat = 'PWS_treatment_fresh_surfacewater_total_bbtu_from_PWS_fresh_surfacewater_withdrawal_total_mgd_intensity'
        expected = convert_kwh_bbtu(405)
        x = output[fsw_treat].mean()
        self.assertAlmostEqual(x, expected, 10)

        sgw_treat = 'PWS_treatment_saline_groundwater_total_bbtu_from_PWS_saline_groundwater_withdrawal_total_mgd_intensity'
        expected = convert_kwh_bbtu(12000)
        x = output[sgw_treat].mean()
        self.assertAlmostEqual(x, expected, 10)

        ssw_treat = 'PWS_treatment_saline_surfacewater_total_bbtu_from_PWS_saline_surfacewater_withdrawal_total_mgd_intensity'
        expected = convert_kwh_bbtu(12000)
        x = output[ssw_treat].mean()
        self.assertAlmostEqual(x, expected, 10)

        fsw_dist = 'PWS_distribution_fresh_surfacewater_total_bbtu_from_PWS_fresh_surfacewater_withdrawal_total_mgd_intensity'
        fgw_dist = 'PWS_distribution_fresh_groundwater_total_bbtu_from_PWS_fresh_groundwater_withdrawal_total_mgd_intensity'
        ssw_dist = 'PWS_distribution_saline_surfacewater_total_bbtu_from_PWS_saline_surfacewater_withdrawal_total_mgd_intensity'
        sgw_dist = 'PWS_distribution_saline_groundwater_total_bbtu_from_PWS_saline_groundwater_withdrawal_total_mgd_intensity'

        expected = convert_kwh_bbtu(1040)
        x = output[fsw_dist].mean()
        self.assertAlmostEqual(x, expected, 10)

        x = output[fgw_dist].mean()
        self.assertAlmostEqual(x, expected, 10)

        x = output[ssw_dist].mean()
        self.assertAlmostEqual(x, expected, 10)

        x = output[sgw_dist].mean()
        self.assertAlmostEqual(x, expected, 10)

    def test_prep_electricity_demand_data(self):

        # collect output
        output = prep_electricity_demand_data()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

        # check that all of the fraction columns are between 0 and 1
        col_list = output.columns[7:].to_list()
        check_list = []
        for col in col_list:
            check_list.append(output[col].max() > 1)
            check_list.append(output[col].min() < 0)
        expected = "True" in check_list
        self.assertEqual(expected, False)

        # make sure US total is not in the dataset
        self.assertFalse("US" in output['State'].to_list())

        # make sure the efficiency values are being appropriately applied
        res_eff = .65  # residential
        com_eff = .65  # commercial
        ind_eff = .49  # industrial
        tra_eff = .21  # transportation
        self.assertTrue(output[output.columns[7]].mean(), 1 - res_eff)
        self.assertTrue(output[output.columns[8]].mean(), res_eff)
        self.assertTrue(output[output.columns[9]].mean(), 1 - com_eff)
        self.assertTrue(output[output.columns[10]].mean(), com_eff)
        self.assertTrue(output[output.columns[11]].mean(), 1 - ind_eff)
        self.assertTrue(output[output.columns[12]].mean(), ind_eff)
        self.assertTrue(output[output.columns[13]].mean(), 1 - tra_eff)
        self.assertTrue(output[output.columns[14]].mean(), tra_eff)

    def test_prep_fuel_demand_data(self):
        # collect output
        output = prep_fuel_demand_data()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

    def test_prep_state_fuel_production_data(self):

        # collect output
        output = prep_state_fuel_production_data()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # test  that there are 51 states accounted for
        output_state = output.groupby("State", as_index=False).sum()
        state_count = output_state['State'].count()
        self.assertEqual(state_count, 51)

        # make sure that removed states are not in state list
        self.assertFalse("X3" in output['State'].to_list())
        self.assertFalse("X5" in output['State'].to_list())
        self.assertFalse("US" in output['State'].to_list())

    def test_prep_county_petroleum_production_data(self):

        # collect output
        output = prep_county_petroleum_production_data()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # make sure that the ratio of unconventional to conventional is correct
        output['frac'] = output['petroleum_unconventional_production_bbtu'] / \
                         (output['petroleum_unconventional_production_bbtu'] +
                          output['petroleum_conventional_production_bbtu'])
        self.assertEqual(output['frac'].mean(), .63)

        # make sure that all of the state percentages add to 1
        output_state = output.groupby("State", as_index=False).sum()
        self.assertEqual(output_state['oil_pct'].mean(), 1)

        # make sure the added Alaska and Idaho counties are correct
        self.assertTrue(output[output.FIPS == '16075']['oil_pct'].mean(), 1)
        self.assertTrue(output[output.FIPS == '02185']['oil_pct'].mean(), .9738)
        self.assertTrue(output[output.FIPS == '02122']['oil_pct'].mean(), .0262)

    def test_prep_petroleum_water_intensity(self):

        # collect output
        output = prep_petroleum_water_intensity()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

        # check that fresh surface water fraction is always .8 for conventional
        conv_output = output[output.con_fsw_frac > 0]
        self.assertAlmostEqual(conv_output['con_fsw_frac'].mean(), .8, 10)

        # check that fresh groundwater fraction is always .2 for conventional
        conv_output = output[output.con_fgw_frac > 0]
        self.assertAlmostEqual(conv_output['con_fgw_frac'].mean(), .2, 10)

        # confirm that output columns match expected
        out_columns = ['FIPS', 'State', 'County', 'un_water_intensity', 'un_fsw_frac', 'un_fgw_frac',
                       'con_water_int', 'con_fsw_frac', 'con_fgw_frac']
        self.assertEqual(out_columns, output.columns.to_list())

    def test_prep_natgas_water_intensity(self):

        # collect output
        output = prep_natgas_water_intensity()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

        # check that for rows with natural gas production, source sum is equal to 1
        output_ng = output[output.natgas_water_intensity > 0].copy()
        output_ng['source_sum'] = output_ng['natgas_fsw_frac'] + output_ng['natgas_fgw_frac']
        self.assertEqual(output_ng['source_sum'].mean(), 1)

    def test_prep_petroleum_gas_discharge_data(self):
        # collect output
        output = prep_petroleum_gas_discharge_data()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

    def test_rename_natgas_petroleum_data(self):
        # collect output
        output = rename_natgas_petroleum_data()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

    def test_prep_county_coal_production_data(self):

        # collect output
        output = prep_county_coal_production_data()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # make sure that the underground mine intensity is the same
        x = output['underground_water_int'].mean()
        self.assertAlmostEqual(x, 0.00144, 10)

        # make sure that the surface mine intensity is the same
        x = output['surface_water_int'].mean()
        self.assertAlmostEqual(x, 0.00034, 10)

    def test_prep_county_coal_data(self):
        # collect output
        output = prep_county_coal_data()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

    def test_remove_double_counting_from_mining(self):

        # collect output
        output = remove_double_counting_from_mining()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

    def test_prep_county_ethanol_production_data(self):

        # collect output
        output = prep_county_ethanol_production_data()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

    def test_remove_industrial_water_double_counting(self):

        # collect output
        output = remove_industrial_water_double_counting()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

    def test_prep_county_water_corn_biomass_data(self):
        # collect output
        output = prep_county_water_corn_biomass_data()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

    def test_remove_irrigation_water_double_counting(self):
        # collect output
        output = remove_irrigation_water_double_counting()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)

        # confirm that output columns match expected
        crop_fsw = 'AGR_crop_fresh_surfacewater_withdrawal_mgd_from_WSW_fresh_surfacewater_total_total_mgd'
        crop_fgw = 'AGR_crop_fresh_groundwater_withdrawal_mgd_from_WSW_fresh_groundwater_total_total_mgd'
        out_columns = ['FIPS', 'State', 'County', crop_fsw, crop_fgw]
        self.assertEqual(out_columns, output.columns.to_list())

    def test_prep_corn_crop_irr_flows(self):
        # collect output
        output = prep_corn_crop_irr_flows()

        # make sure there are no blank values
        is_nan = output.isnull()
        row_has_nan = is_nan.any(axis=1)
        rows_with_nan = output[row_has_nan]
        result = len(rows_with_nan)
        self.assertEqual(result, 0)

        # check that there are the correct number of counties
        output_county_count = len(output['FIPS'])
        expected_county_county = 3142
        self.assertEqual(output_county_count, expected_county_county)



if __name__ == '__main__':
    unittest.main()
