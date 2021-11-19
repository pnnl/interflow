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

        # ensure data columns are type float
        df_float = df[:,3:]
        self.assertEqual(df_float.columns.dtype, 'float')


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

if __name__ == '__main__':
    unittest.main()
