from dataclasses import dataclass
from collections import OrderedDict
from typing import Dict, TypeAlias

from IntPolynumber import IntPolynumber


@dataclass
class RationalPolynumber:
    numerator: IntPolynumber
    denominator: IntPolynumber

    def __repr__(self):
        return f"RationalPolynumber({self.numerator} / {self.denominator})"

    def _clean(self):
        one = IntPolynumber({(0,): 1})
        if self.denominator != one:
            result = self.numerator / self.denominator
            if isinstance(result, IntPolynumber):
                self.numerator, self.denominator = result, one
        return self

    # def __post_init__(self):
    #     self._clean()

    def __bool__(self):
        return bool(self.numerator)

    def __eq__(self, other):
        self = self._clean()
        # can compare RationalPolynumber to Int
        if isinstance(other, int):
            return self == RationalPolynumber(IntPolynumber({(0,): other}), IntPolynumber({(0,): 1}))

        # can compare RationalPolynumber to an IntPolynumber
        if isinstance(other, IntPolynumber):
            other = other._clean()
            return self == RationalPolynumber(other, IntPolynumber({(0,): 1}))

        # can compare RationalPolynumber to a RationalPolynumber
        if isinstance(other, RationalPolynumber):
            other = other._clean()
            numers_match = self.numerator == other.numerator
            denoms_match = self.denominator == other.denominator
            return numers_match and denoms_match

        # cannot compare RationalPolynumber to other types
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        # can add RationalPolynumber with Int
        if isinstance(other, int):
            incoming = IntPolynumber({(0,): other})
            return self + incoming

        # can add RationalPolynumber with IntPolynumber
        if isinstance(other, IntPolynumber):
            incoming = RationalPolynumber(other, IntPolynumber({(0,): 1}))
            return self + incoming

        # can add RationalPolynumber with RationalPolynumber
        # a/b + c/d = (ad + bc) / bd
        if isinstance(other, RationalPolynumber):
            a, b = self.numerator, self.denominator
            c, d = other.numerator, other.denominator
            return ((a * d) + (b * c)) / (b * d)

    def __radd__(self, other):
        return self.__add(other)

    def __sub__(self, other):
        return self + (other * -1)

    def __rsub__(self, other):
        return (self * -1) + other

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        # can multiply RationalPolynumber to an integer
        # a/b * c = a*c/b
        if isinstance(other, int):
            self = self._clean()
            return RationalPolynumber(other * self.numerator, self.denominator)

        # can multiply RationalPolynumber to IntPolynumber
        # a/b * c = a*c/b
        if isinstance(other, IntPolynumber):
            self, other = self._clean(), other._clean()
            return RationalPolynumber(other * self.numerator, self.denominator)

        # can multiply RationaPolynumber to IntPolynumber
        # a/b * c/d = a*b/c*d
        if isinstance(other, RationalPolynumber):
            return RationalPolynumber(self.numerator * other.numerator, self.denominator * other.denominator)

    def __pow__(self, other):
        if not isinstance(other, int):
            raise TypeError(f"Exponent must be int, got {type(other).__name__}")

        accum = 1
        for i in range(other):
            accum = accum * self
        return accum

    def __truediv__(self, other):
        self = self._clean()

        # cant divide by 0
        if not other:
            return NotImplemented

        # can divide RationalPolynumber by a nonzero integer
        # a/b / c = a/b*c
        if isinstance(other, int):
            return RationalPolynumber(self.numerator, self.denominator * other)

        # can divide RationalPolynumber by an IntPolynumber
        # a/b / c = a/b*c
        if isinstance(other, IntPolynumber):
            if not other.coeffs:
                return NotImplemented
            return RationalPolynumber(self.numerator, self.denominator * other)

        # can divide RationalPolynumber by a RationalPolynumber
        # a/b / c/d = a*d/b*c
        if isinstance(other, RationalPolynumber):
            if not self.denominator.coeffs or not other.numerator.coeffs:
                return NotImplemented
            return RationalPolynumber(self.numerator * other.denominator, self.denominator * other.numerator)

    def __call__(self, val):
        if isinstance(val, int):
            numerator = sum(v * val ** e[0] for e, v in self.numerator.coeffs.items())
            denominator = sum(v * val ** e[0] for e, v in self.denominator.coeffs.items())
            return numerator/denominator
        
        return NotImplemented
