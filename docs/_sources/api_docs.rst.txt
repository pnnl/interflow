*********************
API Documentation
*********************

Modules and Functions
----------------------

.. automodule:: interflow.analyze
      :members:

.. automodule:: interflow.calc_flow
      :members:

.. automodule:: interflow.construct
      :members:

.. automodule:: interflow.deconstruct
      :members:

.. automodule:: interflow.reader
      :members:

.. automodule:: interflow.sample_data
      :members:

.. automodule:: interflow.visualize
      :members:


Test Validation Suite
----------------------

**interflow** contains automated tests for checking correctness. Tests are automatically run using pytest, a unittest framework, with Github Actions anytime a push or a pull request is made. Test files developed for **interflow** can also be run locally as individual scripts using the unittest module. All test scripts and can be found in the `tests folder <https://github.com/pnnl/interflow/tree/main/interflow/tests>`_ in the **interflow** repository. For more information on unittest and instructions on how to run test files through the command line see the `unittest documentation <https://docs.python.org/3/library/unittest.html>`_

Below are short descriptions of some of the test cases within the test suite. This is not intended to be an exhaustive list of tests included in the package but instead provides a general idea of the types of tests included. To see the test files for the package, visit the test directory linked above.

**test_analyze.py** - Includes tests for functions of analyze.py. Tests to make sure function returns the expected data structure (e.g., Pandas DataFrame), that grouping results at various levels gives expected DataFrame shape, and that grouping data at various levels through parameter inputs gives the correct sum of data values in the output.

**test_calc_flow.py** - Includes tests for functions of calc_flow.py. There are various types of tests within test_cal_flow.py including:

* tests to confirm that a ValueError gets raised if incorrect input data is provided (e.g., invalid output granularity specified, invalid region name specified, incorrect input data shape provided)
* tests that specifying a desired output level as a parameter gives the expected output granularity
* tests various combinations of sample data values to check that output flows are calculated as expected

**test_construct.py** - Includes tests for functions of construct.py including:

* tests to confirm that a ValueError gets raised if incorrect input data is provided (e.g., invalid input DataFrame shape)
* tests that the output is in the expected format (e.g., Pandas DataFrame)
* tests that the output is at the expected level of data granularity.

**test_deconstruct.py** - Includes tests for functions of construct.py including the following:

* tests that the output is in the expected data format (e.g., Pandas DataFrame)
* tests that tabular output DataFrames are the expected shape
* tests to make sure there are no missing values in output
* tests to confirm that a ValueError gets raised if incorrect input data is provided (e.g., invalid input data structure)

**test_reader.py** - Includes tests for functions of reader.py. Functions within reader are used to read in data files for use in other functions. Each of the functions in reader.py, therefore, are tested to make sure they are loading the input file and returning the expected data structure type.

**test_sample_data.py** - Includes tests for functions of sample_data.py. The functions within sample_data.py collect and organize the US county sample input data provided with the package. The tests of these functions can vary given that each function handles different sample data organization components. Some of the general types of tests included in test_sample_data.py are:

* tests of conversion functions to confirm they are correctly converting units
* tests that output DataFrames have the expected shape
* tests to make sure no data is missing in output DataFrames
* tests to make sure that removed data items do not appear in output DataFrames
* tests to make sure that output DataFrames include the expected columns
* tests to make sure that values in output DataFrames are within the expected range (e.g., fractions fall between 0 and 1, inclusive)
* tests that when functions are run with default parameters that the output is as expected
