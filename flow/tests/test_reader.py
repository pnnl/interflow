# import unittest
#
# from flow.reader import *
#
#
# class TestReader(unittest.TestCase):
#     """Conduct test for functions of reader.py."""
#
#     def test_reader(self):
#         """Ensure we get a dataframe as output."""
#
#         # load the data
#         df = read_input_data()
#
#         # returns a str
#         self.assertTrue(type(df) == pd.DataFrame)
#
#         # first column is a string
#         self.assertTrue(type(df.columns[0]) == 'str')
#
#
# if __name__ == '__main__':
#     unittest.main()
