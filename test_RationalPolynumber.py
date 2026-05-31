import pytest
from random import randint
from collections import OrderedDict
from fractions import Fraction

from Polynumber import RationalPolynumber


class TestRationalPolynumberInstantiation:
    """Test RationalPolynumber instantiation"""

    def test_create_simple_RationalPolynumber(self):
        """Test creating a simple RationalPolynumber"""
        coeffs = {
            (Fraction(1,2),): Fraction(2,3),
            (1,): 2
        }
        poly = RationalPolynumber(coeffs)
        assert poly.coeffs == {(Fraction(1,2),): Fraction(2,3), (Fraction(1,1),): Fraction(2,1)}

    def test_create_empty_RationalPolynumber(self):
        """Test creating an empty RationalPolynumber"""
        coeffs = {}
        poly = RationalPolynumber(coeffs)
        assert poly.coeffs == {}

    def test_create_RationalPolynumber_with_single_int_term(self):
        """Test creating a RationalPolynumber with a single term"""
        coeffs = {(2,): 5}
        poly = RationalPolynumber(coeffs)
        assert poly.coeffs == {(2,): 5}

    def test_create_RationalPolynumber_with_single_fraction_term(self):
        """Test creating a RationalPolynumber with a single term"""
        coeffs = {(Fraction(2,3),): Fraction(5,1)}
        poly = RationalPolynumber(coeffs)
        assert poly.coeffs == {(Fraction(2,3),): Fraction(5,1)}

    def test_RationalPolynumber_filters_zero_coefficients(self):
        """Test that zero coefficients are filtered out"""
        coeffs = {(Fraction(0,1),): Fraction(0,1), (1,): 2}
        poly = RationalPolynumber(coeffs)
        assert (0,) not in poly.coeffs
        assert poly.coeffs == {(1,): 2}

    def test_RationalPolynumber_errors_string_keys(self):
        """Test that string keys cause Error"""
        coeffs = {"invalid": 5}
        with pytest.raises(TypeError):
            poly = RationalPolynumber(coeffs)

    def test_RationalPolynumber_errors_float_keys(self):
        """Test that float keys cause Error"""
        coeffs = {(1.34123,): 5}
        with pytest.raises(TypeError):
            poly = RationalPolynumber(coeffs)

    def test_RationalPolynumber_errors_float_values(self):
        """Test that float values cause Error"""
        coeffs = {(1,): 5.1234}
        with pytest.raises(TypeError):
            poly = RationalPolynumber(coeffs)

    def test_correctly_reorders_coefficients(self):
        """Test creating a RationalPolynumber with float coefficients"""
        coeffs = {(9, 1): 4, (4,): 8, (4, 1): 1, (9,): 15, (Fraction(1,500),): 1}
        poly = RationalPolynumber(coeffs)
        assert poly.coeffs == {(Fraction(1,500),): 1, (4,): 8, (4, 1): 1, (9,): 15, (9, 1): 4}

    def test_RationalPolynumber_repr(self):
        """Test the string representation of a RationalPolynumber"""
        coeffs = {(1,): 2, (0,): 3}
        poly = RationalPolynumber(coeffs)
        assert str(poly) == "RationalPolynumber({(Fraction(0, 1),): Fraction(3, 1), (Fraction(1, 1),): Fraction(2, 1)})"

    def test_accepts_ordered_int_dict(self):
        """Test if OrderdedDict int arguments are accepted"""
        coeffs = OrderedDict({(1,): 2, (0,): 3})
        poly = RationalPolynumber(coeffs)
        assert str(poly) == str(RationalPolynumber({(0,): 3, (1,): 2}))

    def test_zero_RationalPolynumber_is_falsey(self):
        """Test that the zero RationalPolynumber is a falsey python value"""
        coeffs = {(1,): 0, (0,): 0, (Fraction(4,3),): 0}
        poly = RationalPolynumber(coeffs)
        assert bool(poly) is False

    def test_RationalPolynumber_with_fraction_exponents(self):
        """Test RationalPolynumber with fractional exponents"""
        coeffs = {
            (Fraction(1, 2),): 3,
            (Fraction(3, 4),): 2
        }
        poly = RationalPolynumber(coeffs)
        assert poly.coeffs == {
            (Fraction(1, 2),): Fraction(3, 1),
            (Fraction(3, 4),): Fraction(2, 1)
        }

    def test_RationalPolynumber_with_fraction_coefficients(self):
        """Test RationalPolynumber with fractional coefficients"""
        coeffs = {
            (1,): Fraction(1, 2),
            (2,): Fraction(3, 4)
        }
        poly = RationalPolynumber(coeffs)
        assert poly.coeffs == {
            (Fraction(1, 1),): Fraction(1, 2),
            (Fraction(2, 1),): Fraction(3, 4)
        }

    def test_RationalPolynumber_with_fraction_exponents_and_coefficients(self):
        """Test RationalPolynumber with both fractional exponents and coefficients"""
        coeffs = {
            (Fraction(1, 2),): Fraction(2, 3),
            (Fraction(2, 3),): Fraction(5, 7),
            (Fraction(3, 2),): Fraction(1, 4)
        }
        poly = RationalPolynumber(coeffs)
        assert len(poly.coeffs) == 3
        assert poly.coeffs[(Fraction(1, 2),)] == Fraction(2, 3)
        assert poly.coeffs[(Fraction(2, 3),)] == Fraction(5, 7)
        assert poly.coeffs[(Fraction(3, 2),)] == Fraction(1, 4)

    def test_RationalPolynumber_int_exponents_are_converted_to_fractions(self):
        """Test that int exponents are converted to Fractions internally"""
        coeffs = {(1,): 2, (3,): 4}
        poly = RationalPolynumber(coeffs)
        # Internally stored as Fractions
        assert all(isinstance(e, tuple) for e in poly.coeffs.keys())
        assert all(isinstance(v, Fraction) for v in poly.coeffs.values())
        for exp_tuple in poly.coeffs.keys():
            assert all(isinstance(e, Fraction) for e in exp_tuple)

class TestRationalPolynumberEquality:
    """Test RationalPolynumber equality operations"""

    def test_equal_RationalPolynumbers(self):
        """Test that identical RationalPolynumbers are equal"""
        poly1 = RationalPolynumber({(0,): 3, (1,): 2})
        poly2 = RationalPolynumber({(0,): 3, (1,): 2})
        assert poly1 == poly2

    def test_unequal_RationalPolynumbers(self):
        """Test that different RationalPolynumbers are not equal"""
        poly1 = RationalPolynumber({(0,): 3, (1,): 2})
        poly2 = RationalPolynumber({(0,): 3, (1,): 5})
        assert poly1 != poly2

    def test_RationalPolynumber_not_equal_to_other_type(self):
        """Test that a RationalPolynumber is not equal to another type"""
        poly = RationalPolynumber({(0,): 3, (1,): 2})
        assert poly != 5
        assert poly != "RationalPolynumber"
        assert poly != [1, 2, 3]

    def test_equal_int_and_RationalPolynumbers(self):
        """Test that identical int and RationalPolynumber"""
        poly1 = RationalPolynumber({(0,): 3})
        int1 = 3
        assert poly1 == int1

    def test_unequal_int_and_RationalPolynumbers(self):
        """Test that identical int and RationalPolynumber"""
        poly1 = RationalPolynumber({(0,): 3})
        int1 = 4
        assert poly1 != int1


class TestRationalPolynumberAddition:
    """Test RationalPolynumber addition operations"""

    def test_add_two_RationalPolynumbers(self):
        """Test adding two RationalPolynumbers"""
        poly1 = RationalPolynumber({(0,): 3, (1,): 2})
        poly2 = RationalPolynumber({(0,): 2, (1,): 1})
        result = poly1 + poly2
        assert result.coeffs == {(0,): 5, (1,): 3}

    def test_add_RationalPolynumbers_with_different_terms(self):
        """Test adding RationalPolynumbers with different terms"""
        poly1 = RationalPolynumber({(0,): 3, (2,): 1})
        poly2 = RationalPolynumber({(1,): 2})
        result = poly1 + poly2
        assert result.coeffs == {(0,): 3, (1,): 2, (2,): 1}

    def test_add_RationalPolynumber_to_zero(self):
        """Test adding a RationalPolynumber to zero RationalPolynumber"""
        poly1 = RationalPolynumber({(0,): 3, (1,): 2})
        poly2 = RationalPolynumber({})
        result = poly1 + poly2
        assert result.coeffs == {(0,): 3, (1,): 2}

    def test_reverse_add_RationalPolynumbers(self):
        """Test reverse addition (radd)"""
        poly1 = RationalPolynumber({(0,): 3, (1,): 2})
        poly2 = RationalPolynumber({(0,): 2, (1,): 1})
        result = poly2.__radd__(poly1)
        assert result.coeffs == {(0,): 5, (1,): 3}

    def test_add_RationalPolynumbers_with_fraction_exponents(self):
        """Test adding RationalPolynumbers with fractional exponents"""
        poly1 = RationalPolynumber({(Fraction(1, 2),): 3, (Fraction(3, 4),): 2})
        poly2 = RationalPolynumber({(Fraction(1, 2),): 1, (Fraction(3, 4),): 4})
        result = poly1 + poly2
        assert result.coeffs == {
            (Fraction(1, 2),): Fraction(4, 1),
            (Fraction(3, 4),): Fraction(6, 1)
        }

    def test_add_RationalPolynumbers_with_fraction_coefficients(self):
        """Test adding RationalPolynumbers with fractional coefficients"""
        poly1 = RationalPolynumber({(1,): Fraction(1, 2), (2,): Fraction(1, 3)})
        poly2 = RationalPolynumber({(1,): Fraction(1, 4), (2,): Fraction(1, 6)})
        result = poly1 + poly2
        assert result.coeffs == {
            (Fraction(1, 1),): Fraction(3, 4),  # 1/2 + 1/4 = 3/4
            (Fraction(2, 1),): Fraction(1, 2)   # 1/3 + 1/6 = 1/2
        }

    def test_add_RationalPolynumbers_mixed_fractions_and_ints(self):
        """Test adding RationalPolynumbers with mixed fraction and int exponents/coefficients"""
        poly1 = RationalPolynumber({
            (Fraction(1, 2),): 2,
            (1,): Fraction(1, 3)
        })
        poly2 = RationalPolynumber({
            (Fraction(1, 2),): Fraction(3, 4),
            (1,): Fraction(2, 3)
        })
        result = poly1 + poly2
        assert result.coeffs == {
            (Fraction(1, 2),): Fraction(11, 4),  # 2 + 3/4 = 11/4
            (Fraction(1, 1),): Fraction(1, 1)    # 1/3 + 2/3 = 1
        }

    def test_add_RationalPolynumber_with_different_fraction_exponents(self):
        """Test adding RationalPolynumbers with different fractional exponents"""
        poly1 = RationalPolynumber({(Fraction(1, 2),): 5})
        poly2 = RationalPolynumber({(Fraction(2, 3),): 3})
        result = poly1 + poly2
        assert result.coeffs == {
            (Fraction(1, 2),): Fraction(5, 1),
            (Fraction(2, 3),): Fraction(3, 1)
        }

    def test_add_RationalPolynumbers_with_non_reduced_fractions(self):
        """Test adding RationalPolynumbers with non-reduced fractions as coefficients"""
        poly1 = RationalPolynumber({(1,): Fraction(2, 4)})  # 2/4 reduces to 1/2
        poly2 = RationalPolynumber({(1,): Fraction(3, 6)})  # 3/6 reduces to 1/2
        result = poly1 + poly2
        # Both reduce to 1/2, so 1/2 + 1/2 = 1
        assert result.coeffs == {(Fraction(1, 1),): Fraction(1, 1)}


class TestRationalPolynumberSubtraction:
    """Test RationalPolynumber subtraction operations"""

    def test_subtract_two_RationalPolynumbers(self):
        """Test subtracting two RationalPolynumbers"""
        poly1 = RationalPolynumber({(0,): 7, (1,): 5})
        poly2 = RationalPolynumber({(0,): 3, (1,): 2})
        result = poly1 - poly2
        assert result.coeffs == {(0,): 4, (1,): 3}

    def test_reverse_subtract_RationalPolynumbers(self):
        """Test reverse subtraction (rsub)"""
        poly1 = RationalPolynumber({(0,): 3, (1,): 2})
        poly2 = RationalPolynumber({(0,): 7, (1,): 5})
        result = poly1.__rsub__(poly2)
        assert result.coeffs == {(0,): 4, (1,): 3}

    def test_subtract_RationalPolynumber_from_zero(self):
        """Test subtracting a RationalPolynumber from zero RationalPolynumber"""
        zero = RationalPolynumber({})
        poly = RationalPolynumber({(0,): 1, (2,): 4})
        result = zero - poly
        assert result.coeffs == {(0,): -1, (2,): -4}

    def test_subtract_RationalPolynumbers_with_fraction_exponents(self):
        """Test subtracting RationalPolynumbers with fractional exponents"""
        poly1 = RationalPolynumber({(Fraction(1, 2),): 5, (Fraction(3, 4),): 8})
        poly2 = RationalPolynumber({(Fraction(1, 2),): 2, (Fraction(3, 4),): 3})
        result = poly1 - poly2
        assert result.coeffs == {
            (Fraction(1, 2),): Fraction(3, 1),
            (Fraction(3, 4),): Fraction(5, 1)
        }

    def test_subtract_RationalPolynumbers_with_fraction_coefficients(self):
        """Test subtracting RationalPolynumbers with fractional coefficients"""
        poly1 = RationalPolynumber({(1,): Fraction(5, 2), (2,): Fraction(7, 3)})
        poly2 = RationalPolynumber({(1,): Fraction(1, 2), (2,): Fraction(1, 3)})
        result = poly1 - poly2
        assert result.coeffs == {
            (Fraction(1, 1),): Fraction(2, 1),  # 5/2 - 1/2 = 4/2 = 2
            (Fraction(2, 1),): Fraction(2, 1)   # 7/3 - 1/3 = 6/3 = 2
        }

    def test_subtract_RationalPolynumbers_mixed_fractions_and_ints(self):
        """Test subtracting RationalPolynumbers with mixed fraction and int exponents/coefficients"""
        poly1 = RationalPolynumber({
            (Fraction(1, 2),): 5,
            (1,): Fraction(5, 3)
        })
        poly2 = RationalPolynumber({
            (Fraction(1, 2),): Fraction(1, 4),
            (1,): Fraction(2, 3)
        })
        result = poly1 - poly2
        assert result.coeffs == {
            (Fraction(1, 2),): Fraction(19, 4),  # 5 - 1/4 = 19/4
            (Fraction(1, 1),): Fraction(1, 1)    # 5/3 - 2/3 = 1
        }

    def test_subtract_RationalPolynumber_with_different_fraction_exponents(self):
        """Test subtracting RationalPolynumbers with different fractional exponents"""
        poly1 = RationalPolynumber({(Fraction(1, 2),): 7})
        poly2 = RationalPolynumber({(Fraction(2, 3),): 2})
        result = poly1 - poly2
        assert result.coeffs == {
            (Fraction(1, 2),): Fraction(7, 1),
            (Fraction(2, 3),): Fraction(-2, 1)
        }

    def test_subtract_RationalPolynumbers_with_non_reduced_fractions(self):
        """Test subtracting RationalPolynumbers with non-reduced fractions as coefficients"""
        poly1 = RationalPolynumber({(1,): Fraction(4, 4)})  # 4/4 reduces to 1
        poly2 = RationalPolynumber({(1,): Fraction(2, 6)})  # 2/6 reduces to 1/3
        result = poly1 - poly2
        # 1 - 1/3 = 2/3
        assert result.coeffs == {(Fraction(1, 1),): Fraction(2, 3)}


class TestRationalPolynumberMultiplication:
    """Test RationalPolynumber multiplication operations"""

    def test_multiply_RationalPolynumber_by_scalar(self):
        """Test multiplying a RationalPolynumber by a scalar"""
        poly = RationalPolynumber({(0,): 3, (1,): 2})
        result = poly * 3
        assert result.coeffs == {(0,): 9, (1,): 6}

    def test_multiply_RationalPolynumber_by_zero(self):
        """Test multiplying a RationalPolynumber by zero"""
        poly = RationalPolynumber({(0,): 3, (1,): 2})
        result = poly * 0
        assert result.coeffs == {}

    def test_reverse_multiply_RationalPolynumber_by_scalar(self):
        """Test reverse multiplication (rmul)"""
        poly = RationalPolynumber({(0,): 3, (1,): 2})
        result = poly.__rmul__(3)
        assert result.coeffs == {(0,): 9, (1,): 6}

    def test_multiply_two_RationalPolynumbers(self):
        """Test multiplying two RationalPolynumbers"""
        poly1 = RationalPolynumber({(1,): 2})  # 2x
        poly2 = RationalPolynumber({(1,): 3})  # 3x
        result = poly1 * poly2
        assert result.coeffs == {(2,): 6}  # 6x^2

    def test_multiply_RationalPolynumber_binomials(self):
        """Test multiplying (x + 1) * (x + 2)"""
        poly1 = RationalPolynumber({(0,): 1, (1,): 1})  # x + 1
        poly2 = RationalPolynumber({(0,): 2, (1,): 1})  # x + 2
        result = poly1 * poly2
        # (x + 1)(x + 2) = x^2 + 3x + 2
        assert result.coeffs == {(0,): 2, (1,): 3, (2,): 1}

    def test_multiply_RationalPolynumber_by_negative_scalar(self):
        """Test multiplying by negative scalar"""
        poly = RationalPolynumber({(0,): 3, (1,): 2})
        result = poly * -1
        assert result.coeffs == {(0,): -3, (1,): -2}

    def test_multiply_two_RationalPolynumbers_many_coeffs(self):
        """Test multiplying two RationalPolynumbers with many coefficients."""
        dim1 = randint(0, 50)
        dim2 = randint(0, 50)
        poly1_coeffs = {(d,): randint(0, 20) for d in range(dim1)}
        poly2_coeffs = {(d,): randint(0, 20) for d in range(dim2)}
        poly1 = RationalPolynumber(poly1_coeffs)
        poly2 = RationalPolynumber(poly2_coeffs)

        expected = {}
        for (e1,), v1 in poly1_coeffs.items():
            for (e2,), v2 in poly2_coeffs.items():
                e = (e1 + e2,)
                expected[e] = expected.get(e, 0) + (v1 * v2)
        expected = {k: v for k, v in expected.items() if v != 0}

        result = poly1 * poly2
        assert result.coeffs == expected

    def test_multiply_RationalPolynumber_by_fraction_scalar(self):
        """Test multiplying a RationalPolynumber by a fraction scalar"""
        poly = RationalPolynumber({(0,): 3, (1,): 2})
        result = poly * Fraction(1, 2)
        assert result.coeffs == {(0,): Fraction(3, 2), (1,): Fraction(1, 1)}

    def test_multiply_RationalPolynumbers_with_fraction_exponents(self):
        """Test multiplying RationalPolynumbers with fractional exponents"""
        poly1 = RationalPolynumber({(Fraction(1, 2),): 2})  # 2x^(1/2)
        poly2 = RationalPolynumber({(Fraction(1, 2),): 3})  # 3x^(1/2)
        result = poly1 * poly2
        # 2x^(1/2) * 3x^(1/2) = 6x^1
        assert result.coeffs == {(Fraction(1, 1),): Fraction(6, 1)}

    def test_multiply_RationalPolynumbers_with_fraction_coefficients(self):
        """Test multiplying RationalPolynumbers with fractional coefficients"""
        poly1 = RationalPolynumber({(1,): Fraction(1, 2), (0,): Fraction(1, 3)})
        poly2 = RationalPolynumber({(1,): Fraction(1, 2)})
        result = poly1 * poly2
        # (1/3 + 1/2 x) * (1/2 x) = (1/3)(1/2 x) + (1/2 x)(1/2 x)
        # = 1/6 x + 1/4 x^2
        assert result.coeffs == {
            (Fraction(1, 1),): Fraction(1, 6),
            (Fraction(2, 1),): Fraction(1, 4)
        }

    def test_multiply_RationalPolynumbers_mixed_fractions_and_ints_exponents(self):
        """Test multiplying RationalPolynumbers with mixed fraction and int exponents"""
        poly1 = RationalPolynumber({(Fraction(1, 2),): 2})  # 2x^(1/2)
        poly2 = RationalPolynumber({(1,): 3})  # 3x
        result = poly1 * poly2
        # 2x^(1/2) * 3x = 6x^(3/2)
        assert result.coeffs == {(Fraction(3, 2),): Fraction(6, 1)}

    def test_multiply_RationalPolynumbers_with_non_reduced_fractions(self):
        """Test multiplying RationalPolynumbers with non-reduced fractions"""
        poly1 = RationalPolynumber({(1,): Fraction(2, 4)})  # 1/2 x
        poly2 = RationalPolynumber({(1,): Fraction(3, 6)})  # 1/2 x
        result = poly1 * poly2
        # (1/2 x) * (1/2 x) = 1/4 x^2
        assert result.coeffs == {(Fraction(2, 1),): Fraction(1, 4)}

    # slow, but good test
    # def test_multiply_two_RationalPolynumbers_many_fraction_coeffs(self):
    #     """Test multiplying two RationalPolynumbers with many coefficients."""
    #     dim1 = randint(0, 50)
    #     dim2 = randint(2, 51)
    #     poly1_coeffs = {(Fraction(d, e),): Fraction(randint(0, 20), randint(1,20)) for d in range(dim1) for e in range(1, dim2)}
    #     poly2_coeffs = {(Fraction(d, e),): Fraction(randint(0, 20), randint(1,20)) for d in range(dim1) for e in range(1, dim2)}
    #     poly1 = RationalPolynumber(poly1_coeffs)
    #     poly2 = RationalPolynumber(poly2_coeffs)

    #     expected = {}
    #     for (e1,), v1 in poly1_coeffs.items():
    #         for (e2,), v2 in poly2_coeffs.items():
    #             e = (e1 + e2,)
    #             expected[e] = expected.get(e, 0) + (v1 * v2)
    #     expected = {k: v for k, v in expected.items() if v != 0}

    #     result = poly1 * poly2
    #     assert result.coeffs == expected

class TestRationalPolynumberDivision:
    """Test RationalPolynumber division operations"""

    def test_divide_RationalPolynumber_by_scalar(self):
        """Test dividing a RationalPolynumber by a scalar"""
        poly = RationalPolynumber({(0,): 9, (1,): 6})
        result = poly / 3
        assert result.coeffs == {(0,): 3, (1,): 2}

    def test_divide_RationalPolynumber_by_weird_type_returns_not_implemented(self):
        """Test dividing a RationalPolynumber by a scalar"""
        poly = RationalPolynumber({(0,): 9, (1,): 6})
        with pytest.raises(TypeError):
            poly / "hello"

    def test_divide_RationalPolynumber_by_zero_scalar_returns_not_implemented(self):
        """Test that dividing by zero returns NotImplemented"""
        poly = RationalPolynumber({(0,): 3, (1,): 2})
        with pytest.raises(TypeError):
            poly / 0

    def test_dividing_zero_RationalPolynumber_by_scalar(self):
        """Test dividing a zero RationalPolynumber by a scalar"""
        poly = RationalPolynumber({})
        result = poly / 5
        assert result.coeffs == {}

    def test_dividing_by_zero_RationalPolynumber_return_not_implemented(self):
        """Test that dividing by zero returns NotImplemented"""
        poly1 = RationalPolynumber({(0,): 3, (1,): 2})
        poly2 = RationalPolynumber({})
        with pytest.raises(TypeError):
            poly1 / poly2

    def test_dividing_zero_RationalPolynumber_by_nonzero_RationalPolynumber(self):
        poly1 = RationalPolynumber({})
        poly2 = RationalPolynumber({(0,): 3, (1,): 2})
        result = poly1 / poly2
        assert result.coeffs == {}

    # def test_divide_negative_RationalPolynumber(self):
    #     poly1 = RationalPolynumber({(0,): -9, (1,): -6})
    #     poly2 = RationalPolynumber({(0,): 3, (1,): 2})
    #     result = poly1 / poly2
    #     assert result.coeffs == {(0,): -3}

    # def test_dividing_positive_RationalPolynumbers(self):
    #     """Test creating 2 large RationalPolynumbers a,b; doing a*b=c, then checking if c/b == a & c/a == b"""
    #     dim1 = randint(1, 6)
    #     dim2 = randint(0, 6)
    #     poly1_coeffs = {(d,): randint(-20, 20) for d in range(dim1)}
    #     poly2_coeffs = {(d,): randint(-20, 20) for d in range(dim2)}
    #     poly1 = RationalPolynumber(poly1_coeffs)
    #     poly2 = RationalPolynumber(poly2_coeffs)
    #     print("poly1:", poly1)
    #     print("poly2:", poly2)
    #     poly3 = poly1 * poly2
    #     print("poly3:", poly3)
    #     assert poly3 / poly1 == poly2

    # def test_dividing_positive_fraction_RationalPolynumbers(self):
    #     """Test creating 2 large RationalPolynumbers a,b; doing a*b=c, then checking if c/b == a & c/a == b"""
    #     dim1 = randint(1, 6)
    #     dim2 = randint(0, 6)
    #     poly1_coeffs = {(d,): randint(-20, 20) for d in range(dim1)}
    #     poly2_coeffs = {(Fraction(d, e),): Fraction(randint(0, 20), randint(1,20)) for d in range(dim1) for e in range(1, dim2)}
    #     poly1 = RationalPolynumber(poly1_coeffs)
    #     poly2 = RationalPolynumber(poly2_coeffs)
    #     print("poly1:", poly1)
    #     print("poly2:", poly2)
    #     poly3 = poly1 * poly2
    #     print("poly3:", poly3)
    #     assert poly3 / poly1 == poly2


    # def test_dividing_large_positive_fractional_RationalPolynumbers(self):
    #     """Test creating 2 large RationalPolynumbers a,b; doing a*b=c, then checking if c/b == a & c/a == b"""
    #     dim1 = randint(1, 6)
    #     dim2 = randint(0, 6)
    #     poly1_coeffs = {(Fraction(d, e),): Fraction(randint(0, 20), randint(1,20)) for d in range(dim2) for e in range(1, dim2)}
    #     poly2_coeffs = {(Fraction(d, e),): Fraction(randint(0, 20), randint(1,20)) for d in range(dim1) for e in range(1, dim2)}
    #     poly1 = RationalPolynumber(poly1_coeffs)
    #     poly2 = RationalPolynumber(poly2_coeffs)
    #     print("poly1:", poly1)
    #     print("poly2:", poly2)
    #     poly3 = poly1 * poly2
    #     print("poly3:", poly3)
    #     assert poly3 / poly1 == poly2

