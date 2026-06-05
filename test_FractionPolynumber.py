import pytest
from random import randint
from collections import OrderedDict
from fractions import Fraction

from FractionPolynumber import FractionPolynumber


class TestFractionPolynumberInstantiation:
    """Test FractionPolynumber instantiation"""

    def test_create_simple_FractionPolynumber(self):
        """Test creating a simple FractionPolynumber"""
        coeffs = {(Fraction(1, 2),): Fraction(2, 3), (1,): 2}
        poly = FractionPolynumber(coeffs)
        assert poly.coeffs == {(Fraction(1, 2),): Fraction(2, 3), (Fraction(1, 1),): Fraction(2, 1)}

    def test_create_empty_FractionPolynumber(self):
        """Test creating an empty FractionPolynumber"""
        coeffs = {}
        poly = FractionPolynumber(coeffs)
        assert poly.coeffs == {}

    def test_create_FractionPolynumber_with_single_int_term(self):
        """Test creating a FractionPolynumber with a single term"""
        coeffs = {(2,): 5}
        poly = FractionPolynumber(coeffs)
        assert poly.coeffs == {(2,): 5}

    def test_create_FractionPolynumber_with_single_fraction_term(self):
        """Test creating a FractionPolynumber with a single term"""
        coeffs = {(Fraction(2, 3),): Fraction(5, 1)}
        poly = FractionPolynumber(coeffs)
        assert poly.coeffs == {(Fraction(2, 3),): Fraction(5, 1)}

    def test_FractionPolynumber_filters_zero_coefficients(self):
        """Test that zero coefficients are filtered out"""
        coeffs = {(Fraction(0, 1),): Fraction(0, 1), (1,): 2}
        poly = FractionPolynumber(coeffs)
        assert (0,) not in poly.coeffs
        assert poly.coeffs == {(1,): 2}

    def test_FractionPolynumber_errors_string_keys(self):
        """Test that string keys cause Error"""
        coeffs = {"invalid": 5}
        with pytest.raises(TypeError):
            poly = FractionPolynumber(coeffs)

    def test_FractionPolynumber_errors_float_keys(self):
        """Test that float keys cause Error"""
        coeffs = {(1.34123,): 5}
        with pytest.raises(TypeError):
            poly = FractionPolynumber(coeffs)

    def test_FractionPolynumber_errors_float_values(self):
        """Test that float values cause Error"""
        coeffs = {(1,): 5.1234}
        with pytest.raises(TypeError):
            poly = FractionPolynumber(coeffs)

    def test_correctly_reorders_coefficients(self):
        """Test creating a FractionPolynumber with float coefficients"""
        coeffs = {(9, 1): 4, (4,): 8, (4, 1): 1, (9,): 15, (Fraction(1, 500),): 1}
        poly = FractionPolynumber(coeffs)
        assert poly.coeffs == {(Fraction(1, 500),): 1, (4,): 8, (4, 1): 1, (9,): 15, (9, 1): 4}

    def test_FractionPolynumber_repr(self):
        """Test the string representation of a FractionPolynumber"""
        coeffs = {(1,): 2, (0,): 3}
        poly = FractionPolynumber(coeffs)
        assert str(poly) == "FractionPolynumber({(Fraction(0, 1),): Fraction(3, 1), (Fraction(1, 1),): Fraction(2, 1)})"

    def test_accepts_ordered_int_dict(self):
        """Test if OrderdedDict int arguments are accepted"""
        coeffs = OrderedDict({(1,): 2, (0,): 3})
        poly = FractionPolynumber(coeffs)
        assert str(poly) == str(FractionPolynumber({(0,): 3, (1,): 2}))

    def test_zero_FractionPolynumber_is_falsey(self):
        """Test that the zero FractionPolynumber is a falsey python value"""
        coeffs = {(1,): 0, (0,): 0, (Fraction(4, 3),): 0}
        poly = FractionPolynumber(coeffs)
        assert bool(poly) is False

    def test_FractionPolynumber_with_fraction_exponents(self):
        """Test FractionPolynumber with fractional exponents"""
        coeffs = {(Fraction(1, 2),): 3, (Fraction(3, 4),): 2}
        poly = FractionPolynumber(coeffs)
        assert poly.coeffs == {(Fraction(1, 2),): Fraction(3, 1), (Fraction(3, 4),): Fraction(2, 1)}

    def test_FractionPolynumber_with_fraction_coefficients(self):
        """Test FractionPolynumber with fractional coefficients"""
        coeffs = {(1,): Fraction(1, 2), (2,): Fraction(3, 4)}
        poly = FractionPolynumber(coeffs)
        assert poly.coeffs == {(Fraction(1, 1),): Fraction(1, 2), (Fraction(2, 1),): Fraction(3, 4)}

    def test_FractionPolynumber_with_fraction_exponents_and_coefficients(self):
        """Test FractionPolynumber with both fractional exponents and coefficients"""
        coeffs = {
            (Fraction(1, 2),): Fraction(2, 3),
            (Fraction(2, 3),): Fraction(5, 7),
            (Fraction(3, 2),): Fraction(1, 4),
        }
        poly = FractionPolynumber(coeffs)
        assert len(poly.coeffs) == 3
        assert poly.coeffs[(Fraction(1, 2),)] == Fraction(2, 3)
        assert poly.coeffs[(Fraction(2, 3),)] == Fraction(5, 7)
        assert poly.coeffs[(Fraction(3, 2),)] == Fraction(1, 4)

    def test_FractionPolynumber_int_exponents_are_converted_to_fractions(self):
        """Test that int exponents are converted to Fractions internally"""
        coeffs = {(1,): 2, (3,): 4}
        poly = FractionPolynumber(coeffs)
        # Internally stored as Fractions
        assert all(isinstance(e, tuple) for e in poly.coeffs.keys())
        assert all(isinstance(v, Fraction) for v in poly.coeffs.values())
        for exp_tuple in poly.coeffs.keys():
            assert all(isinstance(e, Fraction) for e in exp_tuple)


class TestFractionPolynumberEquality:
    """Test FractionPolynumber equality operations"""

    def test_equal_FractionPolynumbers(self):
        """Test that identical FractionPolynumbers are equal"""
        poly1 = FractionPolynumber({(0,): 3, (1,): 2})
        poly2 = FractionPolynumber({(0,): 3, (1,): 2})
        assert poly1 == poly2

    def test_unequal_FractionPolynumbers(self):
        """Test that different FractionPolynumbers are not equal"""
        poly1 = FractionPolynumber({(0,): 3, (1,): 2})
        poly2 = FractionPolynumber({(0,): 3, (1,): 5})
        assert poly1 != poly2

    def test_FractionPolynumber_not_equal_to_other_type(self):
        """Test that a FractionPolynumber is not equal to another type"""
        poly = FractionPolynumber({(0,): 3, (1,): 2})
        assert poly != 5
        assert poly != "FractionPolynumber"
        assert poly != [1, 2, 3]

    def test_equal_int_and_FractionPolynumbers(self):
        """Test that identical int and FractionPolynumber"""
        poly1 = FractionPolynumber({(0,): 3})
        int1 = 3
        assert poly1 == int1

    def test_unequal_int_and_FractionPolynumbers(self):
        """Test that identical int and FractionPolynumber"""
        poly1 = FractionPolynumber({(0,): 3})
        int1 = 4
        assert poly1 != int1


class TestFractionPolynumberAddition:
    """Test FractionPolynumber addition operations"""

    def test_add_two_FractionPolynumbers(self):
        """Test adding two FractionPolynumbers"""
        poly1 = FractionPolynumber({(0,): 3, (1,): 2})
        poly2 = FractionPolynumber({(0,): 2, (1,): 1})
        result = poly1 + poly2
        assert result.coeffs == {(0,): 5, (1,): 3}

    def test_add_FractionPolynumbers_with_different_terms(self):
        """Test adding FractionPolynumbers with different terms"""
        poly1 = FractionPolynumber({(0,): 3, (2,): 1})
        poly2 = FractionPolynumber({(1,): 2})
        result = poly1 + poly2
        assert result.coeffs == {(0,): 3, (1,): 2, (2,): 1}

    def test_add_FractionPolynumber_to_zero(self):
        """Test adding a FractionPolynumber to zero FractionPolynumber"""
        poly1 = FractionPolynumber({(0,): 3, (1,): 2})
        poly2 = FractionPolynumber({})
        result = poly1 + poly2
        assert result.coeffs == {(0,): 3, (1,): 2}

    def test_reverse_add_FractionPolynumbers(self):
        """Test reverse addition (radd)"""
        poly1 = FractionPolynumber({(0,): 3, (1,): 2})
        poly2 = FractionPolynumber({(0,): 2, (1,): 1})
        result = poly2.__radd__(poly1)
        assert result.coeffs == {(0,): 5, (1,): 3}

    def test_add_FractionPolynumbers_with_fraction_exponents(self):
        """Test adding FractionPolynumbers with fractional exponents"""
        poly1 = FractionPolynumber({(Fraction(1, 2),): 3, (Fraction(3, 4),): 2})
        poly2 = FractionPolynumber({(Fraction(1, 2),): 1, (Fraction(3, 4),): 4})
        result = poly1 + poly2
        assert result.coeffs == {(Fraction(1, 2),): Fraction(4, 1), (Fraction(3, 4),): Fraction(6, 1)}

    def test_add_FractionPolynumbers_with_fraction_coefficients(self):
        """Test adding FractionPolynumbers with fractional coefficients"""
        poly1 = FractionPolynumber({(1,): Fraction(1, 2), (2,): Fraction(1, 3)})
        poly2 = FractionPolynumber({(1,): Fraction(1, 4), (2,): Fraction(1, 6)})
        result = poly1 + poly2
        assert result.coeffs == {
            (Fraction(1, 1),): Fraction(3, 4),  # 1/2 + 1/4 = 3/4
            (Fraction(2, 1),): Fraction(1, 2),  # 1/3 + 1/6 = 1/2
        }

    def test_add_FractionPolynumbers_mixed_fractions_and_ints(self):
        """Test adding FractionPolynumbers with mixed fraction and int exponents/coefficients"""
        poly1 = FractionPolynumber({(Fraction(1, 2),): 2, (1,): Fraction(1, 3)})
        poly2 = FractionPolynumber({(Fraction(1, 2),): Fraction(3, 4), (1,): Fraction(2, 3)})
        result = poly1 + poly2
        assert result.coeffs == {
            (Fraction(1, 2),): Fraction(11, 4),  # 2 + 3/4 = 11/4
            (Fraction(1, 1),): Fraction(1, 1),  # 1/3 + 2/3 = 1
        }

    def test_add_FractionPolynumber_with_different_fraction_exponents(self):
        """Test adding FractionPolynumbers with different fractional exponents"""
        poly1 = FractionPolynumber({(Fraction(1, 2),): 5})
        poly2 = FractionPolynumber({(Fraction(2, 3),): 3})
        result = poly1 + poly2
        assert result.coeffs == {(Fraction(1, 2),): Fraction(5, 1), (Fraction(2, 3),): Fraction(3, 1)}

    def test_add_FractionPolynumbers_with_non_reduced_fractions(self):
        """Test adding FractionPolynumbers with non-reduced fractions as coefficients"""
        poly1 = FractionPolynumber({(1,): Fraction(2, 4)})  # 2/4 reduces to 1/2
        poly2 = FractionPolynumber({(1,): Fraction(3, 6)})  # 3/6 reduces to 1/2
        result = poly1 + poly2
        # Both reduce to 1/2, so 1/2 + 1/2 = 1
        assert result.coeffs == {(Fraction(1, 1),): Fraction(1, 1)}


class TestFractionPolynumberSubtraction:
    """Test FractionPolynumber subtraction operations"""

    def test_subtract_two_FractionPolynumbers(self):
        """Test subtracting two FractionPolynumbers"""
        poly1 = FractionPolynumber({(0,): 7, (1,): 5})
        poly2 = FractionPolynumber({(0,): 3, (1,): 2})
        result = poly1 - poly2
        assert result.coeffs == {(0,): 4, (1,): 3}

    def test_reverse_subtract_FractionPolynumbers(self):
        """Test reverse subtraction (rsub)"""
        poly1 = FractionPolynumber({(0,): 3, (1,): 2})
        poly2 = FractionPolynumber({(0,): 7, (1,): 5})
        result = poly1.__rsub__(poly2)
        assert result.coeffs == {(0,): 4, (1,): 3}

    def test_subtract_FractionPolynumber_from_zero(self):
        """Test subtracting a FractionPolynumber from zero FractionPolynumber"""
        zero = FractionPolynumber({})
        poly = FractionPolynumber({(0,): 1, (2,): 4})
        result = zero - poly
        assert result.coeffs == {(0,): -1, (2,): -4}

    def test_subtract_FractionPolynumbers_with_fraction_exponents(self):
        """Test subtracting FractionPolynumbers with fractional exponents"""
        poly1 = FractionPolynumber({(Fraction(1, 2),): 5, (Fraction(3, 4),): 8})
        poly2 = FractionPolynumber({(Fraction(1, 2),): 2, (Fraction(3, 4),): 3})
        result = poly1 - poly2
        assert result.coeffs == {(Fraction(1, 2),): Fraction(3, 1), (Fraction(3, 4),): Fraction(5, 1)}

    def test_subtract_FractionPolynumbers_with_fraction_coefficients(self):
        """Test subtracting FractionPolynumbers with fractional coefficients"""
        poly1 = FractionPolynumber({(1,): Fraction(5, 2), (2,): Fraction(7, 3)})
        poly2 = FractionPolynumber({(1,): Fraction(1, 2), (2,): Fraction(1, 3)})
        result = poly1 - poly2
        assert result.coeffs == {
            (Fraction(1, 1),): Fraction(2, 1),  # 5/2 - 1/2 = 4/2 = 2
            (Fraction(2, 1),): Fraction(2, 1),  # 7/3 - 1/3 = 6/3 = 2
        }

    def test_subtract_FractionPolynumbers_mixed_fractions_and_ints(self):
        """Test subtracting FractionPolynumbers with mixed fraction and int exponents/coefficients"""
        poly1 = FractionPolynumber({(Fraction(1, 2),): 5, (1,): Fraction(5, 3)})
        poly2 = FractionPolynumber({(Fraction(1, 2),): Fraction(1, 4), (1,): Fraction(2, 3)})
        result = poly1 - poly2
        assert result.coeffs == {
            (Fraction(1, 2),): Fraction(19, 4),  # 5 - 1/4 = 19/4
            (Fraction(1, 1),): Fraction(1, 1),  # 5/3 - 2/3 = 1
        }

    def test_subtract_FractionPolynumber_with_different_fraction_exponents(self):
        """Test subtracting FractionPolynumbers with different fractional exponents"""
        poly1 = FractionPolynumber({(Fraction(1, 2),): 7})
        poly2 = FractionPolynumber({(Fraction(2, 3),): 2})
        result = poly1 - poly2
        assert result.coeffs == {(Fraction(1, 2),): Fraction(7, 1), (Fraction(2, 3),): Fraction(-2, 1)}

    def test_subtract_FractionPolynumbers_with_non_reduced_fractions(self):
        """Test subtracting FractionPolynumbers with non-reduced fractions as coefficients"""
        poly1 = FractionPolynumber({(1,): Fraction(4, 4)})  # 4/4 reduces to 1
        poly2 = FractionPolynumber({(1,): Fraction(2, 6)})  # 2/6 reduces to 1/3
        result = poly1 - poly2
        # 1 - 1/3 = 2/3
        assert result.coeffs == {(Fraction(1, 1),): Fraction(2, 3)}


class TestFractionPolynumberMultiplication:
    """Test FractionPolynumber multiplication operations"""

    def test_multiply_FractionPolynumber_by_scalar(self):
        """Test multiplying a FractionPolynumber by a scalar"""
        poly = FractionPolynumber({(0,): 3, (1,): 2})
        result = poly * 3
        assert result.coeffs == {(0,): 9, (1,): 6}

    def test_multiply_FractionPolynumber_by_zero(self):
        """Test multiplying a FractionPolynumber by zero"""
        poly = FractionPolynumber({(0,): 3, (1,): 2})
        result = poly * 0
        assert result.coeffs == {}

    def test_reverse_multiply_FractionPolynumber_by_scalar(self):
        """Test reverse multiplication (rmul)"""
        poly = FractionPolynumber({(0,): 3, (1,): 2})
        result = poly.__rmul__(3)
        assert result.coeffs == {(0,): 9, (1,): 6}

    def test_multiply_two_FractionPolynumbers(self):
        """Test multiplying two FractionPolynumbers"""
        poly1 = FractionPolynumber({(1,): 2})  # 2x
        poly2 = FractionPolynumber({(1,): 3})  # 3x
        result = poly1 * poly2
        assert result.coeffs == {(2,): 6}  # 6x^2

    def test_multiply_FractionPolynumber_binomials(self):
        """Test multiplying (x + 1) * (x + 2)"""
        poly1 = FractionPolynumber({(0,): 1, (1,): 1})  # x + 1
        poly2 = FractionPolynumber({(0,): 2, (1,): 1})  # x + 2
        result = poly1 * poly2
        # (x + 1)(x + 2) = x^2 + 3x + 2
        assert result.coeffs == {(0,): 2, (1,): 3, (2,): 1}

    def test_multiply_FractionPolynumber_by_negative_scalar(self):
        """Test multiplying by negative scalar"""
        poly = FractionPolynumber({(0,): 3, (1,): 2})
        result = poly * -1
        assert result.coeffs == {(0,): -3, (1,): -2}

    def test_multiply_two_FractionPolynumbers_many_coeffs(self):
        """Test multiplying two FractionPolynumbers with many coefficients."""
        dim1 = randint(0, 50)
        dim2 = randint(0, 50)
        poly1_coeffs = {(d,): randint(0, 20) for d in range(dim1)}
        poly2_coeffs = {(d,): randint(0, 20) for d in range(dim2)}
        poly1 = FractionPolynumber(poly1_coeffs)
        poly2 = FractionPolynumber(poly2_coeffs)

        expected = {}
        for (e1,), v1 in poly1_coeffs.items():
            for (e2,), v2 in poly2_coeffs.items():
                e = (e1 + e2,)
                expected[e] = expected.get(e, 0) + (v1 * v2)
        expected = {k: v for k, v in expected.items() if v != 0}

        result = poly1 * poly2
        assert result.coeffs == expected

    def test_multiply_FractionPolynumber_by_fraction_scalar(self):
        """Test multiplying a FractionPolynumber by a fraction scalar"""
        poly = FractionPolynumber({(0,): 3, (1,): 2})
        result = poly * Fraction(1, 2)
        assert result.coeffs == {(0,): Fraction(3, 2), (1,): Fraction(1, 1)}

    def test_multiply_FractionPolynumbers_with_fraction_exponents(self):
        """Test multiplying FractionPolynumbers with fractional exponents"""
        poly1 = FractionPolynumber({(Fraction(1, 2),): 2})  # 2x^(1/2)
        poly2 = FractionPolynumber({(Fraction(1, 2),): 3})  # 3x^(1/2)
        result = poly1 * poly2
        # 2x^(1/2) * 3x^(1/2) = 6x^1
        assert result.coeffs == {(Fraction(1, 1),): Fraction(6, 1)}

    def test_multiply_FractionPolynumbers_with_fraction_coefficients(self):
        """Test multiplying FractionPolynumbers with fractional coefficients"""
        poly1 = FractionPolynumber({(1,): Fraction(1, 2), (0,): Fraction(1, 3)})
        poly2 = FractionPolynumber({(1,): Fraction(1, 2)})
        result = poly1 * poly2
        # (1/3 + 1/2 x) * (1/2 x) = (1/3)(1/2 x) + (1/2 x)(1/2 x)
        # = 1/6 x + 1/4 x^2
        assert result.coeffs == {(Fraction(1, 1),): Fraction(1, 6), (Fraction(2, 1),): Fraction(1, 4)}

    def test_multiply_FractionPolynumbers_mixed_fractions_and_ints_exponents(self):
        """Test multiplying FractionPolynumbers with mixed fraction and int exponents"""
        poly1 = FractionPolynumber({(Fraction(1, 2),): 2})  # 2x^(1/2)
        poly2 = FractionPolynumber({(1,): 3})  # 3x
        result = poly1 * poly2
        # 2x^(1/2) * 3x = 6x^(3/2)
        assert result.coeffs == {(Fraction(3, 2),): Fraction(6, 1)}

    def test_multiply_FractionPolynumbers_with_non_reduced_fractions(self):
        """Test multiplying FractionPolynumbers with non-reduced fractions"""
        poly1 = FractionPolynumber({(1,): Fraction(2, 4)})  # 1/2 x
        poly2 = FractionPolynumber({(1,): Fraction(3, 6)})  # 1/2 x
        result = poly1 * poly2
        # (1/2 x) * (1/2 x) = 1/4 x^2
        assert result.coeffs == {(Fraction(2, 1),): Fraction(1, 4)}

    # slow, but good test
    # def test_multiply_two_FractionPolynumbers_many_fraction_coeffs(self):
    #     """Test multiplying two FractionPolynumbers with many coefficients."""
    #     dim1 = randint(0, 50)
    #     dim2 = randint(2, 51)
    #     poly1_coeffs = {(Fraction(d, e),): Fraction(randint(0, 20), randint(1,20)) for d in range(dim1) for e in range(1, dim2)}
    #     poly2_coeffs = {(Fraction(d, e),): Fraction(randint(0, 20), randint(1,20)) for d in range(dim1) for e in range(1, dim2)}
    #     poly1 = FractionPolynumber(poly1_coeffs)
    #     poly2 = FractionPolynumber(poly2_coeffs)

    #     expected = {}
    #     for (e1,), v1 in poly1_coeffs.items():
    #         for (e2,), v2 in poly2_coeffs.items():
    #             e = (e1 + e2,)
    #             expected[e] = expected.get(e, 0) + (v1 * v2)
    #     expected = {k: v for k, v in expected.items() if v != 0}

    #     result = poly1 * poly2
    #     assert result.coeffs == expected


class TestFractionPolynumberDivision:
    """Test FractionPolynumber division operations"""

    def test_divide_FractionPolynumber_by_scalar(self):
        """Test dividing a FractionPolynumber by a scalar"""
        poly = FractionPolynumber({(0,): 9, (1,): 6})
        result = poly / 3
        assert result.coeffs == {(0,): 3, (1,): 2}

    def test_divide_FractionPolynumber_by_weird_type_returns_not_implemented(self):
        """Test dividing a FractionPolynumber by a scalar"""
        poly = FractionPolynumber({(0,): 9, (1,): 6})
        with pytest.raises(TypeError):
            poly / "hello"

    def test_divide_FractionPolynumber_by_zero_scalar_returns_not_implemented(self):
        """Test that dividing by zero returns NotImplemented"""
        poly = FractionPolynumber({(0,): 3, (1,): 2})
        with pytest.raises(TypeError):
            poly / 0

    def test_dividing_zero_FractionPolynumber_by_scalar(self):
        """Test dividing a zero FractionPolynumber by a scalar"""
        poly = FractionPolynumber({})
        result = poly / 5
        assert result.coeffs == {}

    def test_dividing_by_zero_FractionPolynumber_return_not_implemented(self):
        """Test that dividing by zero returns NotImplemented"""
        poly1 = FractionPolynumber({(0,): 3, (1,): 2})
        poly2 = FractionPolynumber({})
        with pytest.raises(TypeError):
            poly1 / poly2

    def test_dividing_zero_FractionPolynumber_by_nonzero_FractionPolynumber(self):
        poly1 = FractionPolynumber({})
        poly2 = FractionPolynumber({(0,): 3, (1,): 2})
        result = poly1 / poly2
        assert result.coeffs == {}

    # def test_divide_negative_FractionPolynumber(self):
    #     poly1 = FractionPolynumber({(0,): -9, (1,): -6})
    #     poly2 = FractionPolynumber({(0,): 3, (1,): 2})
    #     result = poly1 / poly2
    #     assert result.coeffs == {(0,): -3}

    # def test_dividing_positive_FractionPolynumbers(self):
    #     """Test creating 2 large FractionPolynumbers a,b; doing a*b=c, then checking if c/b == a & c/a == b"""
    #     dim1 = randint(1, 6)
    #     dim2 = randint(0, 6)
    #     poly1_coeffs = {(d,): randint(-20, 20) for d in range(dim1)}
    #     poly2_coeffs = {(d,): randint(-20, 20) for d in range(dim2)}
    #     poly1 = FractionPolynumber(poly1_coeffs)
    #     poly2 = FractionPolynumber(poly2_coeffs)
    #     print("poly1:", poly1)
    #     print("poly2:", poly2)
    #     poly3 = poly1 * poly2
    #     print("poly3:", poly3)
    #     assert poly3 / poly1 == poly2

    # def test_dividing_positive_fraction_FractionPolynumbers(self):
    #     """Test creating 2 large FractionPolynumbers a,b; doing a*b=c, then checking if c/b == a & c/a == b"""
    #     dim1 = randint(1, 6)
    #     dim2 = randint(0, 6)
    #     poly1_coeffs = {(d,): randint(-20, 20) for d in range(dim1)}
    #     poly2_coeffs = {(Fraction(d, e),): Fraction(randint(0, 20), randint(1,20)) for d in range(dim1) for e in range(1, dim2)}
    #     poly1 = FractionPolynumber(poly1_coeffs)
    #     poly2 = FractionPolynumber(poly2_coeffs)
    #     print("poly1:", poly1)
    #     print("poly2:", poly2)
    #     poly3 = poly1 * poly2
    #     print("poly3:", poly3)
    #     assert poly3 / poly1 == poly2

    # def test_dividing_large_positive_fractional_FractionPolynumbers(self):
    #     """Test creating 2 large FractionPolynumbers a,b; doing a*b=c, then checking if c/b == a & c/a == b"""
    #     dim1 = randint(1, 6)
    #     dim2 = randint(0, 6)
    #     poly1_coeffs = {(Fraction(d, e),): Fraction(randint(0, 20), randint(1,20)) for d in range(dim2) for e in range(1, dim2)}
    #     poly2_coeffs = {(Fraction(d, e),): Fraction(randint(0, 20), randint(1,20)) for d in range(dim1) for e in range(1, dim2)}
    #     poly1 = FractionPolynumber(poly1_coeffs)
    #     poly2 = FractionPolynumber(poly2_coeffs)
    #     print("poly1:", poly1)
    #     print("poly2:", poly2)
    #     poly3 = poly1 * poly2
    #     print("poly3:", poly3)
    #     assert poly3 / poly1 == poly2
