import unittest

from flow.clean import *
from flow.reader import *

class TestClean(unittest.TestCase):
    """Conduct test for functions of clean.py."""

    def test_prep_water_use_2015(self):
        """Ensure we get what is expected from prep_water_use_2015()."""

        # load data
        df = prep_water_use_2015()

        # expected number of columns
        self.assertEqual(df.columns.shape[0], 26)

        # FIPS code is a string
        self.assertTrue(df['FIPS'].dtype, 'str')

        # ensure data columns are type float
        df_float = df.iloc[:, 3:]
        self.assertTrue(df_float.columns.dtype, 'float')

        # no null data rows
        rows_with_null = [index for index, row in df.iterrows() if row.isnull().any()]
        self.assertEqual(rows_with_null, [])

if __name__ == '__main__':
    unittest.main()
