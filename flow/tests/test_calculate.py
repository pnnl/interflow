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
        data = configure_data()
        parameters = get_electricity_generation_efficiency_parameters()
        df = calc_electricity_generation_energy_discharge(data, parameters)


        # test that the output has the correct number of columns and rows
        self.assertEqual(df.shape[0], data.shape[0])

        # test that the total across regions for rejected energy is equal to fuel - energy services
        test_dict = construct_nested_dictionary(get_electricity_generation_efficiency_parameters())  # load parameter dictionary
        test_fuel_type = list(test_dict.keys())[0]  # generate test fuel_type from first key in dictionary
        test_sub_fuel_type = list(test_dict[test_fuel_type].keys())[0]  # generate test sub_fuel_type from first key

        fuel_input_total_name = f'ec_consumption_{test_fuel_type}_{test_sub_fuel_type}_to_eg_generation_bbtu'
        energy_services_total_name = f'eg_generation_{test_fuel_type}_{test_sub_fuel_type}_to_re_bbtu'
        rejected_energy_total_name = f'eg_generation_{test_fuel_type}_{test_sub_fuel_type}_to_es_bbtu'

        rejected_energy_output_value = df[rejected_energy_total_name].sum()
        rejected_energy_test_value = df[fuel_input_total_name].sum() - df[energy_services_total_name].sum()

        self.assertAlmostEqual(rejected_energy_test_value, rejected_energy_output_value, 2)

        # test that the rejected energy within a single region is equal to fuel - energy services
        rejected_energy_output_value = df[rejected_energy_total_name][10]
        rejected_energy_test_value = df[fuel_input_total_name][10] - df[energy_services_total_name][10]
        self.assertAlmostEqual(rejected_energy_test_value, rejected_energy_output_value, 2)

        # test that the total energy services is equal to fuel - rejected energy
        energy_services_output_value = df[energy_services_total_name].sum()
        energy_services_test_value = df[fuel_input_total_name].sum() - df[rejected_energy_total_name].sum()
        self.assertAlmostEqual(energy_services_test_value, energy_services_output_value, 2)

        # test that the rejected energy within a single region is equal to fuel - energy services
        energy_services_output_value = df[energy_services_total_name][10]
        energy_services_test_value = df[fuel_input_total_name][10] - df[rejected_energy_total_name][10]
        self.assertAlmostEqual(energy_services_test_value, energy_services_output_value, 2)

        # test that there are no blank rows
        is_NaN = df.isnull()
        row_has_NaN = is_NaN.any(axis=1)
        rows_with_NaN = df[row_has_NaN]
        self.assertEqual(rows_with_NaN.shape[0], 0)

        # test that having the incorrect number of columns in parameter data raises a ValueError
        fail_parameter_data = get_electricity_generation_efficiency_parameters()
        fail_parameter_data = fail_parameter_data.drop(fail_parameter_data.columns[2], axis=1)
        with self.assertRaises(ValueError):
            calc_electricity_generation_energy_discharge(data, fail_parameter_data)


if __name__ == '__main__':
    unittest.main()
