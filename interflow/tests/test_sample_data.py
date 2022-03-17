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

if __name__ == '__main__':
    unittest.main()
