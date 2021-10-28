import unittest

from flow.sample import add


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


if __name__ == '__main__':
    unittest.main()
