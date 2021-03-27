# Purpose: provide limited-possible-value types.
from enum import Enum
from typing import Any, Dict, Union


class LimitNames(Enum):
    """
    All types of Limits.
    """

    SIGNED_PERCENTAGE = 0
    UNSIGNED_PERCENTAGE = 1


class BaseLimit:
    def __init__(self, supports_silent_assert: bool = False):
        """
        Initialize a base limit.

        :param supports_silent_assert: whether this Limit can handle failed asserts by adjusting values to match
            limitations.
        """

        self._supports_silent_assert = supports_silent_assert

    def assert_value(self, value, use_silent_assert: bool = False):
        """
        Assert the specified value is valid for the limit sub-class.

        :param value: value to assert the validity of.
        :param use_silent_assert: whether to suse the supports_silent_assert capability when asserting the value
            of this Limit.
        """

        raise NotImplementedError("This method must be implemented by child classes.")


class NumericLimit(BaseLimit):
    """
    Define numeric Limits, inclusive.
    For example::

        lim = NumericLimit(min_value=0, max_value=100)
        lim.assert_value(0)     # Valid!
        lim.assert_value(100)   # Valid too!
        lim.assert_value(101)   # Raises AssertionError!

    Another example::

        lim = NumericLimit(min_value=-100, max_value=100, use_silent_assert=True)
        lim.assert_value(0)     # Valid!
        lim.assert_value(100)   # Valid too!
        lim.assert_value(101)   # Returns 100!
        lim.assert_value(-142)  # Returns -100!
    """

    def __init__(self, min_value=None, max_value=None):
        """
        Initialize a new numeric limit.

        :param min_value: minimum value for the limit, inclusive. May be None if max_value is not.
        :param max_value: maximum value for the limit, inclusive. May be None if min_value is not.
        """

        super().__init__(supports_silent_assert=True)

        if min_value is None and max_value is None:
            raise ValueError("min_value and max_value can't both be None.")

        self._min_value = min_value
        self._max_value = max_value

    def assert_value(self, value, use_silent_assert: bool = False):
        """
        Assert the specified value is valid to this Limit.
        :param value: value to check the validity of.
        :param use_silent_assert: whether to return, without raising an exception, the closest valid value to the
            invalid value specified, if that's the case.
        :return: None if a valid value provided; otherwise, the closest valid value to the invalid value specified.
        :raise AssertionError: if use_silent_assert is False and an invalid value is specified.
        """

        if self._min_value and self._max_value is None:
            if value < self._min_value:
                if use_silent_assert:
                    return self._min_value
                else:
                    raise AssertionError(f"Expected value {value} >= {self._min_value}, got otherwise.")

        if self._max_value and self._min_value is None:
            if value > self._max_value:
                if use_silent_assert:
                    return self._max_value
                else:
                    raise AssertionError(f"Expected value {value} <= {self._max_value}, got otherwise.")

        if value < self._min_value or value > self._max_value:
            if use_silent_assert:
                return self._min_value if value < self._min_value else self._max_value
            else:
                raise AssertionError(
                    f"Expected value in range {self._min_value} <= {value} <= {self._max_value}, got otherwise.")


class ListLimit(BaseLimit):
    """
    Define iterable Limits. This Limit doesn't support Silent Asserts.
    For example::

        lim = NumericLimit([1, 2, 4, 8])
        lim.assert_limit(2)     # Valid!
        lim.assert_limit(3)     # Raises AssertionError!
    """

    def __init__(self, valid_items: Union[list, set]):
        """
        Initialize a new list Limit.
        :param valid_items: a list or a set of valid items.
        """

        super(ListLimit, self).__init__(supports_silent_assert=False)

        if isinstance(valid_items, list) or isinstance(valid_items, set):
            self._valid_items = valid_items
        else:
            raise TypeError("valid_items must be a list or a set.")

    def assert_value(self, value, use_silent_assert: bool = False):
        assert value in self._valid_items, f"Expected {value} to be a valid item, got otherwise."


class Limits:
    """
    Define supported limits.
    """

    LIMITS: Dict[LimitNames, BaseLimit] = {
        LimitNames.SIGNED_PERCENTAGE: NumericLimit(min_value=-100, max_value=+100),
        LimitNames.UNSIGNED_PERCENTAGE: NumericLimit(min_value=0, max_value=+100),
    }
    """
    Dictionary containing all available limits.
    """

    @staticmethod
    def assert_limit(limit: LimitNames, value: Any):
        Limits.LIMITS[limit].assert_value(value)
