import unittest
from flow.clean import *
from flow.reader import *
from flow.configure import *
from flow.calculate import *
from flow.construct import *

class TestCalculate(unittest.TestCase):
    """Conduct test for functions of calculate.py."""

    def test_calc_electricity_generation_energy_discharge(self):
        # load data
        df = calc_electricity_generation_energy_discharge(data=configure_data())

        # test that
        self.assertEqual(df.columns.shape[0], 30)


if __name__ == '__main__':
    unittest.main()
