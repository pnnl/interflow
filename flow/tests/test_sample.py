import unittest

import pandas as pd

from flow.sample import add, fake_df


class TestSample(unittest.TestCase):
    """Test the functionality of the sample code."""

    def test_add(self):
        """Ensure that add produces what we expect."""

        # test for failure on string arguement
        with self.assertRaises(TypeError):
            add(x='a', y='b')

        # test result pass
        result = add(1, 2.2)
        expected = 3.2
        self.assertEqual(result, expected)

    def test_fake_df(self):
        """asdf"""

        d = {'a': [1, 2, 3], 'b': [4.4, 5, 7.7]}
        expected_df = pd.DataFrame(d)

        df = fake_df()

        pd.testing.assert_frame_equal(expected_df, df)


if __name__ == '__main__':
    unittest.main()
