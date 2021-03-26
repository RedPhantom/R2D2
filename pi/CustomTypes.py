# Purpose: contain custom object types.

# TODO: Transition from custom classes to NewType() + a Limits class.

class LimitedSignedPercentage:
    """
    Define the behavior of a signed (positive or negative) limited percentage - a value which cannot exceed
    defined thresholds.
    """

    MIN_VALUE = -100
    MAX_VALUE = +100

    def __init__(self, value: int):
        LimitedSignedPercentage._assert_valid(value)

        self._value: int = int(value)

    def __add__(self, other):
        if isinstance(other, LimitedSignedPercentage):
            return LimitedSignedPercentage(self._safe_add(self._value, other._value))

        return self._safe_add(self._value, other)

    def __iadd__(self, other):
        if isinstance(other, LimitedSignedPercentage):
            self._value = self._safe_add(self._value, other._value)
        else:
            self._value = self._safe_add(self._value, other)

        return self

    def __sub__(self, other):
        if isinstance(other, LimitedSignedPercentage):
            return LimitedSignedPercentage(self._safe_sub(self._value, other._value))

        return self._safe_sub(self._value, other)

    def __isub__(self, other):
        if isinstance(other, LimitedSignedPercentage):
            self._value = self._safe_sub(self._value, other._value)
        else:
            self._value = self._safe_sub(self._value, other)

    def __mul__(self, other):
        if isinstance(other, LimitedSignedPercentage):
            op_result = self._value * other._value
        else:
            op_result = self._value * other

        if op_result > self.MAX_VALUE:
            return LimitedSignedPercentage(self.MAX_VALUE)

        if op_result < self.MIN_VALUE:
            return LimitedSignedPercentage(self.MIN_VALUE)

        self._value = op_result
        return self

    def __divmod__(self, other):
        raise NotImplementedError()

    def __int__(self):
        return self._value

    def __float__(self):
        return float(self._value)

    def __str__(self):
        return f"{self._value}%"

    def __repr__(self):
        return f"{self.__class__}({self._value})"

    @staticmethod
    def _safe_add(val1: int, val2: int):
        max_val = LimitedSignedPercentage.MAX_VALUE
        return min([max_val, val1 + val2])

    @staticmethod
    def _safe_sub(val1: int, val2: int):
        min_val = LimitedSignedPercentage.MIN_VALUE
        return max([min_val, val1 - val2])

    @staticmethod
    def _assert_valid(value):
        min_val = LimitedSignedPercentage.MIN_VALUE
        max_val = LimitedSignedPercentage.MAX_VALUE
        if value < min_val or value > max_val:
            raise ValueError(f"The value {value} exceeds the limited {min_val} - {max_val} range.")
