# Purpose: contain unit tests for custom types.

import unittest

from Limits import NumericLimit


class BasicSanity(unittest.TestCase):
    def test_numeric_limit_loud(self):
        """
        Test the NumericLimits' loud functionality.
        """

        min_value = 0
        max_value = 100
        valid_value = (max_value - min_value) / 2
        invalid_values = [max_value + 1, min_value - 1]
        numeric_limit = NumericLimit(min_value=min_value, max_value=max_value)

        print("Asserting valid value", valid_value)
        numeric_limit.assert_value(valid_value)

        for invalid_value in invalid_values:
            print("Asserting invalid value", invalid_value)

            with self.assertRaises(AssertionError):
                numeric_limit.assert_value(invalid_value)

    def test_numeric_limit_silent(self):
        """
        Test the NumericLimits' silent functionality.
        """

        min_value = 0
        max_value = 100
        values = [(min_value, min_value - 1), (max_value, max_value + 1)]

        numeric_limit = NumericLimit(min_value=min_value, max_value=max_value)

        for valid_value, invalid_value in values:
            print("Asserting invalid value", invalid_value, "is silently set to valid value", valid_value)
            self.assertEqual(valid_value, numeric_limit.assert_value(invalid_value, use_silent_assert=True))
