import unittest

from flow.clean import *
from flow.reader import *

class TestClean(unittest.TestCase):
    """Conduct test for functions of clean.py."""

    def test_prep_water_use_2015(self):
        """Ensure we get what is expected from prep_water_use_2015()."""

        # load data
        df = prep_water_use_2015(all_variables = True)

        # expected number of columns
        self.assertEqual(df.columns.shape[0], 30)

        # string variables are strings
        #df_str = df.iloc[:, :2]
        #self.assertEqual(df_str.columns.dtype, 'O')

        # ensure data columns are type float
        self.assertEqual(df['FIPS'].dtype, 'O')


        # no null data rows
        rows_with_null = [index for index, row in df.iterrows() if row.isnull().any()]
        self.assertEqual(rows_with_null, [])

    def test_prep_water_use_1995(self):
        """Ensure we get what is expected from prep_water_use_1995()."""

        # load data
        df = prep_water_use_1995()

        # expected number of columns
        self.assertEqual(df.columns.shape[0], 36)

        # ensure data columns are type float
        self.assertEqual(df["FIPS"].dtypes, 'O')

        # no null data rows
        rows_with_null = [index for index, row in df.iterrows() if row.isnull().any()]
        self.assertEqual(rows_with_null, [])

    def test_prep_wastewater_data(self):
        """Ensure we get what is expected from the county identifier data."""

        # load data
        df = get_county_identifier_data()

        # no null data rows
        rows_with_null = [index for index, row in df.iterrows() if row.isnull().any()]
        self.assertEqual(rows_with_null, [])

        # ensure FIPS column is type float
        self.assertEqual(df["FIPS"].dtypes, 'O')

        # load data
        df = prep_wastewater_data()

        # no null data rows
        rows_with_null = [index for index, row in df.iterrows() if row.isnull().any()]
        self.assertEqual(rows_with_null, [])

        # ensure FIPS column is type float
        self.assertEqual(df["FIPS"].dtypes, 'O')

        # ensure total wastewater is sum of infiltration and non-infiltration
        self.assertAlmostEqual(df["EXIST_AVG"].sum() + df["EXIST_INFILTRATION"].sum(),
                               df["EXIST_TOTAL"].sum(),
                               delta=1)

        # ensure all discharge water is equal to total water processed
        col_list = ['ww_evap', 'ww_gd', 'ww_in', 'ww_ir', 'ww_od',
                    'ww_ps', 'ww_sd', 'ww_ww']
        self.assertAlmostEqual(df[col_list].sum(axis=1).sum(),
                               df["EXIST_TOTAL"].sum(),
                               delta=1)

        # ensure all treated water is equal to total water processed
        col_list = ['no_treatment', 'ww_adv', 'ww_prim', 'ww_sec']
        self.assertAlmostEqual(df[col_list].sum(axis=1).sum(),
                               df["EXIST_TOTAL"].sum(),
                               delta=1)



if __name__ == '__main__':
    unittest.main()
