from dataclasses import dataclass
from collections import OrderedDict
from typing import Dict, TypeAlias

from fractions import Fraction

FractionExponents: TypeAlias = tuple[Fraction, ...]
FractionCoefficient: TypeAlias = Fraction
FractionCoeffDict: TypeAlias = OrderedDict[FractionExponents, FractionCoefficient]


@dataclass
class FractionPolynumber:
    coeffs: FractionCoeffDict  # {(Fraction exponent,): Fraction value}, }

    def __repr__(self):
        return f"FractionPolynumber({dict(self.coeffs)})"

    def _clean(self):
        """Create a normalize form. Convert to Fractions, remove zeros, sort."""
        # Only accept int or Fraction types
        for exp, val in self.coeffs.items():
            if not isinstance(exp, tuple):
                raise TypeError(f"Exponent key must be a tuple, got {type(exp).__name__}")
            if not isinstance(val, (int, Fraction)):
                raise TypeError(f"Coefficient must be int or Fraction, got {type(val).__name__}")
            for e in exp:
                if not isinstance(e, (int, Fraction)):
                    raise TypeError(f"Exponent must be int or Fraction, got {type(e).__name__}")

        filtered = {tuple(Fraction(e) for e in exp): Fraction(val) for exp, val in self.coeffs.items() if val != 0}

        self.coeffs = FractionCoeffDict(sorted(filtered.items()))
        return self

    def __post_init__(self):
        return self._clean()

    def __bool__(self):
        return bool(self.coeffs)

    def __eq__(self, other):
        # can compare FractionPolynumber to Int
        if isinstance(other, int):
            return FractionPolynumber({(0,): other}) == self

        if isinstance(other, FractionPolynumber):
            self, other = self._clean(), other._clean()
            return self.coeffs == other.coeffs

        # cannot compare FractionPolynumber to other types
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        # can add FractionPolynumber with Int
        if isinstance(other, int):
            incoming = FractionPolynumber({(0,): other})
            return self + incoming

        # can add FractionPolynumber with FractionPolynumber
        if isinstance(other, FractionPolynumber):
            self, other = self._clean(), other._clean()
            all_coeff_keys = {*self.coeffs.keys(), *other.coeffs.keys()}

            # 1D case
            if not any(len(k) > 1 for k in all_coeff_keys):
                return FractionPolynumber({c: (self.coeffs.get(c, 0) + other.coeffs.get(c, 0)) for c in all_coeff_keys})

            # 2D+ case.  not yet implemented
            if any(len(k) > 1 for k in all_coeff_keys):
                return NotImplemented

        # cannot add FractionPolynumber to other types
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self + (other * -1)

    def __rsub__(self, other):
        return (self * -1) + other

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        # can multiply FractionPolynumber to an integer
        if isinstance(other, (int, Fraction)):
            self = self._clean()
            return FractionPolynumber({e: (v * other) for e, v in self.coeffs.items()})

        # can multiply FractionPolynumber to FractionPolynumber
        if isinstance(other, FractionPolynumber):
            self, other = self._clean(), other._clean()
            all_coeff_keys = {*self.coeffs.keys(), *other.coeffs.keys()}

            # 1D case
            if not any(len(k) > 1 for k in all_coeff_keys):
                # parts will be {sum of exponent pair: [product of a value pair, product of next value pair]}
                parts = {}
                for e1, v1 in self.coeffs.items():
                    for e2, v2 in other.coeffs.items():
                        exponent_pair = e1[0] + e2[0]
                        value_pair = v1 * v2
                        if not parts.get(exponent_pair):
                            parts[exponent_pair] = [value_pair]
                        else:
                            parts[exponent_pair].append(value_pair)
                return FractionPolynumber({(e,): sum(v) for e, v in parts.items()})

            # 2D+ case.  not yet implemented
            if any(len(k) > 1 for k in all_coeff_keys):
                return NotImplemented

        # cannot multiply FractionPolynumber other types
        return NotImplemented

    def __pow__(self, other):
        if isinstance(other, int):
            exp = other
        elif isinstance(other, Fraction):
            # Accept Fractions that are whole numbers
            if other.denominator == 1:
                exp = other.numerator
            else:
                raise TypeError(
                    f"Exponent must be a whole number, got Fraction({other.numerator}, {other.denominator})"
                )
        else:
            raise TypeError(f"Exponent must be int or whole-number Fraction, got {type(other).__name__}")

        accum = 1
        for i in range(exp):
            accum = accum * self
        return accum

    def __truediv__(self, other):
        self = self._clean()

        # cant divide by 0
        if not other:
            return NotImplemented

        # can divide FractionPolynumber by a nonzero integer or fraction
        if isinstance(other, (int, Fraction)):
            new = FractionPolynumber({e: int(v / other) for e, v in self.coeffs.items()})
            return new

        if isinstance(other, FractionPolynumber):
            other = other._clean()
            # cant divide by the 0 FractionPolynumber
            if not other.coeffs:
                return NotImplemented

            # zero FractionPolynumber divided by anything nonzero is a zero FractionPolynumber
            if not self.coeffs and other.coeffs:
                return FractionPolynumber({})

            all_coeff_keys = {*self.coeffs.keys(), *other.coeffs.keys()}

            # 2D+ case.  not yet implemented
            if isinstance(other, FractionPolynumber) and any(len(k) > 1 for k in all_coeff_keys):
                return NotImplemented

            # 1D case
            if isinstance(other, FractionPolynumber) and not any(len(k) > 1 for k in all_coeff_keys):
                # not sure how to do long division when "shift" can be a Fraction
                return NotImplemented

                # doing long division slightly backward.
                # example in base10 with commas between digit places:
                # i.e, 243 = 3159/13
                #          2, 4,3       quotent = {dimen: mult, dimen: mult, dimen, mult} = 2,4,3
                # 1,3 / 2,10,15,9       divisor/dividend
                #             3,9       mult * divisor * slider**shift == 3 * 13 * 10**0
                #       2,10,12,        remainder
                #          4,12         mult * divisor * slider**shift == 4 * 13 * 10**1
                #       2, 6,           remainder
                #       2, 6            mult * divisor * slider**shift == 3 * 13 * 10**0
                #       0               remainder
                dividend, divisor = self, other
                parts = {}
                while dividend.coeffs:
                    # while dividend.coeffs, we're sliding the divisor each loop
                    e_dividend, v_dividend = next(iter(dividend.coeffs.items()))
                    e_divisor, v_divisor = next(iter(divisor.coeffs.items()))
                    mult = v_dividend / v_divisor
                    if mult != round(mult):
                        # we cant handle floats in values yet
                        return NotImplemented
                    mult = round(mult)
                    shift = e_dividend[0] - e_divisor[0]
                    dimen = (shift,)
                    # stash the quotient so far in parts = {dimen: [mult, mult...], }
                    parts.setdefault(dimen, []).append(mult)
                    # multiplying by slider does shift all the FractionPolynumber's values up by an exponent
                    slider = FractionPolynumber({(1,): 1})
                    remainder = dividend - (mult * divisor * slider**shift)
                    # dividend in next round is the remainder
                    dividend = remainder
                quotent = FractionPolynumber({e: sum(v) for e, v in parts.items()})
                # return quotent

        # cannot divide FractionPolynumber by other types
        return NotImplemented

    def __call__(self, val):
        if isinstance(val, int):
            return sum(v * val ** e[0] for e, v in self.coeffs.items())

        return NotImplemented
