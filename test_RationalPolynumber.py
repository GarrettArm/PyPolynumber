import pytest
from random import randint
from collections import OrderedDict
from IntPolynumber import IntPolynumber
from RationalPolynumber import RationalPolynumber


def _ip(d):
    return IntPolynumber(d)


def _rp(num_d, denom_d):
    return RationalPolynumber(_ip(num_d), _ip(denom_d))


class TestRationalPolynumberInstantiation:
    """Test RationalPolynumber instantiation"""

    def test_repr(self):
        """Test that repr shows numerator / denominator"""
        num = IntPolynumber({(3,): 2, (0,): 4})  # 2x^3 + 4
        denom = IntPolynumber({(2,): 1, (0,): -5})  # x^2 - 5
        r = RationalPolynumber(num, denom)
        assert repr(r) == "RationalPolynumber(IntPolynumber({(0,): 4, (3,): 2}) / IntPolynumber({(0,): -5, (2,): 1}))"

    def test_create_simple_rationalpolynumber(self):
        """Test creating a simple RationalPolynumber stores numerator and denominator"""
        num = _ip({(0,): 1, (1,): 1})  # x + 1
        denom = _ip({(0,): -1, (1,): 1})  # x - 1
        r = RationalPolynumber(num, denom)
        assert r.numerator == num
        assert r.denominator == denom

    def test_zero_numerator_is_falsey(self):
        """Test that a RationalPolynumber with zero numerator is falsey"""
        r = _rp({}, {(0,): 1})
        assert bool(r) is False

    def test_nonzero_rationalpolynumber_is_truthy(self):
        """Test that a RationalPolynumber with nonzero numerator is truthy"""
        r = _rp({(0,): 3}, {(0,): 1})
        assert bool(r) is True

    def test_reduction_during_creation(self):
        """(2x^2 + x - 3)/(2x + 3) reduces to (x - 1)/1"""
        num = _ip({(0,): -3, (1,): 1, (2,): 2})
        denom = _ip({(0,): 3, (1,): 2})
        r = RationalPolynumber(num, denom)
        assert r == RationalPolynumber(_ip({(0,): -1, (1,): 1}), _ip({(0,): 1}))

    def test_rationalpolynumber_call_with_int(self):
        """Test evaluating a RationalPolynumber at an integer: (2x + 1)/(x + 1) at x=1 == 1.5"""
        r = _rp({(0,): 1, (1,): 2}, {(0,): 1, (1,): 1})  # (2x + 1)/(x + 1)
        assert r(1) == 1.5

    def test_not_equal_to_other_type(self):
        """Test that RationalPolynumber is not equal to non-numeric types"""
        r = _rp({(0,): 3}, {(0,): 1})
        assert r != "hello"
        assert r != [1, 2, 3]


class TestRationalPolynumberEquality:
    """Test RationalPolynumber equality operations"""

    def test_equal_rationalpolynumbers(self):
        """Test that identical RationalPolynumbers are equal"""
        polyrat1 = RationalPolynumber(_ip({(0,): 1, (1,): -5}), _ip({(3,): 4, (7,): 13}))
        polyrat2 = polyrat1
        assert polyrat1 == polyrat2

    def test_unequal_rationalpolynumbers(self):
        """Test that different RationalPolynumbers are not equal"""
        r1 = _rp({(0,): 1}, {(0,): 2})  # 1/2
        r2 = _rp({(0,): 1}, {(0,): 3})  # 1/3
        assert r1 != r2

    def test_equal_after_reduction(self):
        """Test that equivalent RationalPolynumbers are equal after reduction"""
        r1 = _rp({(0,): -3, (1,): 1, (2,): 2}, {(0,): 3, (1,): 2})  # (2x^2+x-3)/(2x+3) == x-1
        r2 = _rp({(0,): -1, (1,): 1}, {(0,): 1})
        assert r1 == r2

    def test_equal_to_integer(self):
        """RationalPolynumber representing a constant equals that integer"""
        r = RationalPolynumber(_ip({(0,): 7}), _ip({(0,): 1}))
        assert r == 7

    def test_not_equal_to_different_integer(self):
        """Test that a constant RationalPolynumber is not equal to a different int"""
        r = _rp({(0,): 5}, {(0,): 1})
        assert r != 6

    def test_equal_to_intpolynumber(self):
        """RationalPolynumber with denominator 1 equals the equivalent IntPolynumber"""
        intpoly = _ip({(0,): -1, (1,): 1})  # x - 1
        r = RationalPolynumber(intpoly, _ip({(0,): 1}))
        assert r == intpoly

    def test_not_equal_to_different_intpolynumber(self):
        """Test inequality with a different IntPolynumber"""
        r = _rp({(0,): -1, (1,): 1}, {(0,): 1})
        assert r != _ip({(0,): -2, (1,): 1})


class TestRationalPolynumberAddition:
    """Test RationalPolynumber addition operations"""

    def test_add_two_rationalpolynumbers(self):
        """Test 1/2 + 1/3 == 5/6"""
        r1 = _rp({(0,): 1}, {(0,): 2})
        r2 = _rp({(0,): 1}, {(0,): 3})
        result = r1 + r2
        assert result == _rp({(0,): 5}, {(0,): 6})

    def test_add_rationalpolynumber_with_int(self):
        """Test (x + 1)/1 + 2 == x + 3"""
        r = _rp({(0,): 1, (1,): 1}, {(0,): 1})
        result = r + 2
        assert result == _ip({(0,): 3, (1,): 1})

    def test_add_rationalpolynumber_with_intpolynumber(self):
        """Test (x + 1)/1 + x == 2x + 1"""
        r = _rp({(0,): 1, (1,): 1}, {(0,): 1})
        p = _ip({(1,): 1})
        result = r + p
        assert result == _ip({(0,): 1, (1,): 2})

    def test_add_rationalpolynumber_to_zero(self):
        """Test adding a rationalpolynumber to the zero rationalpolynumber"""
        r = _rp({(0,): 3, (1,): 2}, {(0,): 1})
        zero = _rp({}, {(0,): 1})
        result = r + zero
        assert result == _ip({(0,): 3, (1,): 2})


class TestRationalPolynumberSubtraction:
    """Test RationalPolynumber subtraction operations"""

    def test_subtract_two_rationalpolynumbers(self):
        """Test 1/2 - 1/3 == 1/6"""
        r1 = _rp({(0,): 1}, {(0,): 2})
        r2 = _rp({(0,): 1}, {(0,): 3})
        result = r1 - r2
        assert result == _rp({(0,): 1}, {(0,): 6})

    def test_subtract_int_from_rationalpolynumber(self):
        """Test (x + 3)/1 - 2 == x + 1"""
        r = _rp({(0,): 3, (1,): 1}, {(0,): 1})
        result = r - 2
        assert result == _ip({(0,): 1, (1,): 1})

    def test_subtract_rationalpolynumber_from_zero(self):
        """Test 0 - 3/1 == -3"""
        zero = _rp({}, {(0,): 1})
        r = _rp({(0,): 3}, {(0,): 1})
        result = zero - r
        assert result == _ip({(0,): -3})

    def test_reverse_subtract_rationalpolynumbers(self):
        """Test r.__rsub__(p) computes p - r: (x - 1) - (x + 1) == -2"""
        r = _rp({(0,): 1, (1,): 1}, {(0,): 1})  # x + 1
        p = _ip({(0,): -1, (1,): 1})  # x - 1
        result = r.__rsub__(p)
        assert result == _ip({(0,): -2})


class TestRationalPolynumberMultiplication:
    """Test RationalPolynumber multiplication operations"""

    def test_multiply_by_scalar(self):
        """Test (x + 1)/2 * 2 == x + 1"""
        r = _rp({(0,): 1, (1,): 1}, {(0,): 2})
        result = r * 2
        assert result == _ip({(0,): 1, (1,): 1})

    def test_multiply_by_zero(self):
        """Test multiplying a rationalpolynumber by zero gives zero"""
        r = _rp({(0,): 3, (1,): 2}, {(0,): 1})
        result = r * 0
        assert result == _rp({}, {(0,): 1})

    def test_reverse_multiply_by_scalar(self):
        """Test reverse multiplication (rmul)"""
        r = _rp({(0,): 1, (1,): 1}, {(0,): 2})
        result = r.__rmul__(2)
        assert result == _ip({(0,): 1, (1,): 1})

    def test_multiply_by_intpolynumber(self):
        """Test (x + 1)/2 * 2 (as IntPolynumber) == x + 1"""
        r = _rp({(0,): 1, (1,): 1}, {(0,): 2})
        p = _ip({(0,): 2})
        result = r * p
        assert result == _ip({(0,): 1, (1,): 1})

    def test_multiply_two_simple_rationalpolynumbers(self):
        """Test 1/2 * 1/3 == 1/6"""
        r1 = _rp({(0,): 1}, {(0,): 2})
        r2 = _rp({(0,): 1}, {(0,): 3})
        result = r1 * r2
        assert result == _rp({(0,): 1}, {(0,): 6})

    def test_multiply_two_rationalpolynumbers(self):
        """Test (2x^2 + x - 3)/(7x^4 + 1) * (x - 1)/(5x^5 + 2) == (3x^2 - x^2 - 4x + 3)/(35x^9 + 5x^5 + 14x^4 + 2)"""
        r1 = _rp({(0,): -3, (1,): 1, (2,): 2}, {(0,): 1, (4,): 7})
        r2 = _rp({(0,): -1, (1,): 1}, {(0,): 2, (5,): 5})
        result = r1 * r2
        assert result == _rp({(0,): 3, (1,): -4, (2,): -1, (3,): 2}, {(0,): 2, (4,): 14, (5,): 5, (9,): 35})

    def test_multiply_rationalpolynumber_by_negative(self):
        """Test multiplying by -1 negates the numerator"""
        r = _rp({(0,): 3, (1,): 2}, {(0,): 1})
        result = r * -1
        assert result == _ip({(0,): -3, (1,): -2})


class TestRationalPolynumberDivision:
    """Test RationalPolynumber division operations"""

    def test_divide_by_scalar(self):
        """Test (2x^2 - 4x)/(5x^5 + 3x^3) / 2 == (2x^2 - 4x)/(10x^5 + 6x^3)"""
        r = _rp({(1,): -4, (2,): 2}, {(3,): 3, (5,): 5})
        result = r / 2
        assert result == _rp({(1,): -4, (2,): 2}, {(3,): 6, (5,): 10})

    def test_divide_by_zero_scalar_raises(self):
        """Test that dividing by zero raises TypeError"""
        r = _rp({(0,): 3, (1,): 2}, {(0,): 1})
        with pytest.raises(TypeError):
            r / 0

    def test_divide_by_intpolynumber(self):
        """Test (2x^2 + x - 3)/1 / (x - 1) == 2x + 3"""
        r = _rp({(0,): -3, (1,): 1, (2,): 2}, {(0,): 1})
        divisor = _ip({(0,): -1, (1,): 1})
        result = r / divisor
        assert result == _rp({(0,): 3, (1,): 2}, {(0,): 1})

    def test_divide_by_rationalpolynumber(self):
        """Test (2x^2 + x - 3)/(3x + 4) / (x-1)/(5x^5 + 2) == (2x^2 + x - 3)*(5x^5 +2) / (x-1)*(3x + 4)"""
        a = _rp({(0,): -3, (1,): 1, (2,): 2}, {(0,): 1})
        b = _rp({(0,): -1, (1,): 1}, {(0,): 2, (5,): 5})
        result = a / b
        assert result == _rp({(0,): -6, (1,): 2, (2,): 4, (5,): -15, (6,): 5, (7,): 10}, {(0,): -1, (1,): 1})

    def test_divide_by_zero_intpolynumber_raises(self):
        """Test that dividing by zero IntPolynumber raises TypeError"""
        r = _rp({(0,): 3, (1,): 2}, {(0,): 1})
        with pytest.raises(TypeError):
            r / _ip({})

    def test_divide_by_zero_rationalpolynumber_raises(self):
        """Test that dividing by zero IntPolynumber raises TypeError"""
        r = _rp({(0,): 3, (1,): 2}, {(0,): 1})
        with pytest.raises(TypeError):
            r / _rp(_ip({}, _ip({(0,): 1})))

    def test_divide_negative_rationalpolynumber(self):
        """Test (-6x - 9)/1 / (2x + 3) == -3"""
        r = _rp({(0,): -9, (1,): -6}, {(0,): 1})
        divisor = _ip({(0,): 3, (1,): 2})
        result = r / divisor
        assert result == _ip({(0,): -3})

    def test_divide_zero_rationalpolynumber_by_scalar(self):
        """Test dividing zero rationalpolynumber by a nonzero scalar gives zero"""
        r = _rp({}, {(0,): 1})
        result = r / 5
        assert result == _rp({}, {(0,): 1})
