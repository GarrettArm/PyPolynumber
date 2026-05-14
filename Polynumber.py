from dataclasses import dataclass
from collections import OrderedDict
from typing import Dict


@dataclass
class Polynumber:
    coeffs: Dict  # {(exponent,): value}, }

    def __repr__(self):
        return str(self.coeffs)

    def _clean(self):
        filtered = {
            k: v
            for k, v in self.coeffs.items()
            if isinstance(k, tuple) and isinstance(k[0], int) and isinstance(v, (int, float)) and v != 0
        }
        self.coeffs = OrderedDict(sorted(filtered.items()))
        return self

    def __post_init__(self):
        return self._clean()

    def __eq__(self, other):
        # cannot compare Polynumber to another type
        if not isinstance(other, Polynumber):
            return False

        self, other = self._clean(), other._clean()
        if self.coeffs == other.coeffs:
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        # cannot add Polynumber to another type
        if not isinstance(other, Polynumber):
            return NotImplemented

        self, other = self._clean(), other._clean()
        all_coeff_keys = {*self.coeffs.keys(), *other.coeffs.keys()}

        # 2D+ case.  not yet implemented
        if any(len(k) > 1 for k in all_coeff_keys):
            return NotImplemented

        # 1D case
        if not any(len(k) > 1 for k in all_coeff_keys):
            return Polynumber({c: (self.coeffs.get(c, 0) + other.coeffs.get(c, 0)) for c in all_coeff_keys})

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self + (other * -1)

    def __rsub__(self, other):
        return (self * -1) + other

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        # can multiply Polynumber to an integer
        if isinstance(other, int):
            self = self._clean()
            return Polynumber({e: (v * other) for e, v in self.coeffs.items()})

        # cannot multiply Polynumber to another type
        if not isinstance(other, Polynumber):
            return NotImplemented

        self, other = self._clean(), other._clean()
        all_coeff_keys = {*self.coeffs.keys(), *other.coeffs.keys()}

        # 2D+ case.  not yet implemented
        if any(len(k) > 1 for k in all_coeff_keys):
            return NotImplemented

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
            return Polynumber({(e,): sum(v) for e, v in parts.items()})

    def __pow__(self, other):
        accum = 1
        for i in range(other):
            accum = accum * self
        return accum

    def __truediv__(self, other):
        self = self._clean()

        # cannot divide Polynumber by most other types
        if not isinstance(other, (Polynumber, int)):
            return NotImplemented

        # cant divide by 0
        if not other:
            return NotImplemented

        # can divide Polynumber by an integer
        if isinstance(other, int):
            new = Polynumber({e: (v / other) for e, v in self.coeffs.items()})
            return new

        # cant divide by the 0 polynumber
        if not other.coeffs:
            return NotImplemented

        # zero polynumber divided by anything nonzero is a zero polynumber
        if not self.coeffs and other.coeffs:
            return Polynumber({})

        other = other._clean()
        all_coeff_keys = {*self.coeffs.keys(), *other.coeffs.keys()}

        # 2D+ case.  not yet implemented
        if isinstance(other, Polynumber) and any(len(k) > 1 for k in all_coeff_keys):
            return NotImplemented

        # 1D case
        if isinstance(other, Polynumber) and not any(len(k) > 1 for k in all_coeff_keys):
            # doing long division slightly backward.
            # example in base10 with commas between digit places:
            # i.e,                  243 = 3159/13 
            #          2, 4,3                quotent = {dimen: mult, dimen: mult, dimen, mult} = 2,4,3
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
                # multiplying by slider does shift all the Polynumber's values up by an exponent
                slider = Polynumber({(1,): 1})
                remainder = dividend - (mult * divisor * slider**shift)
                # dividend in next round is the remainder
                dividend = remainder
            quotent = Polynumber({e: sum(v) for e, v in parts.items()})
            return quotent

    def __call__(self, val):
        if isinstance(val, int):
            return sum(v * val ** e[0] for e, v in self.coeffs.items())

        return NotImplemented
