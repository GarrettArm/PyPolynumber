import pytest
from random import randint
from collections import OrderedDict
from Polynumber import Polynumber


class TestPolynumberInstantiation:
    """Test Polynumber instantiation"""

    def test_create_simple_polynomial(self):
        """Test creating a simple polynomial"""
        coeffs = {(0,): 3, (1,): 2}
        poly = Polynumber(coeffs)
        assert poly.coeffs == {(0,): 3, (1,): 2}

    def test_create_empty_polynomial(self):
        """Test creating an empty polynomial"""
        coeffs = {}
        poly = Polynumber(coeffs)
        assert poly.coeffs == {}

    def test_create_polynomial_with_single_term(self):
        """Test creating a polynomial with a single term"""
        coeffs = {(2,): 5}
        poly = Polynumber(coeffs)
        assert poly.coeffs == {(2,): 5}

    def test_polynomial_filters_zero_coefficients(self):
        """Test that zero coefficients are filtered out"""
        coeffs = {(0,): 0, (1,): 2, (2,): 3}
        poly = Polynumber(coeffs)
        assert (0,) not in poly.coeffs
        assert poly.coeffs == {(1,): 2, (2,): 3}

    def test_polynomial_filters_invalid_keys(self):
        """Test that invalid keys are filtered out"""
        coeffs = {(0,): 3, (1,): 2, "invalid": 5}
        poly = Polynumber(coeffs)
        assert "invalid" not in poly.coeffs
        assert len(poly.coeffs) == 2

    def test_polynomial_filters_invalid_values(self):
        """Test that invalid values are filtered out"""
        coeffs = {(0,): "invalid", (1,): 2, (2,): 3}
        poly = Polynumber(coeffs)
        assert (0,) not in poly.coeffs
        assert poly.coeffs == {(1,): 2, (2,): 3}

    def test_polynomial_with_float_coefficients(self):
        """Test creating a polynomial with float coefficients"""
        coeffs = {(0,): 3.7, (1,): 2.5}
        poly = Polynumber(coeffs)
        assert poly.coeffs == {(0,): 3.7, (1,): 2.5}

    def test_correctly_reorders_coefficients(self):
        """Test creating a polynomial with float coefficients"""
        coeffs = {(9, 1): 4, (4,): 8, (4, 1): 1, (9,): 15}
        poly = Polynumber(coeffs)
        assert poly.coeffs == {(4,): 8, (4, 1): 1, (9,): 15, (9, 1): 4}

    def test_polynomial_repr(self):
        """Test the string representation of a polynomial"""
        coeffs = {(1,): 2, (0,): 3}
        poly = Polynumber(coeffs)
        assert str(poly) == str(OrderedDict({(0,): 3, (1,): 2}))

    def test_polynomial_repr_inverse(self):
        """Test the string representation of a polynomial"""
        coeffs = {(1,): 2, (0,): 3}
        poly = Polynumber(coeffs)
        assert str(poly) != str(OrderedDict({(1,): 2, (0,): 3}))

    def test_accepts_ordered_dict(self):
        """Test if OrderdedDict arguments are accepted"""
        coeffs = OrderedDict({(1,): 2, (0,): 3})
        poly = Polynumber(coeffs)
        assert str(poly) == str(OrderedDict({(0,): 3, (1,): 2}))


class TestPolynumberEquality:
    """Test Polynumber equality operations"""

    def test_equal_polynomials(self):
        """Test that identical polynomials are equal"""
        poly1 = Polynumber({(0,): 3, (1,): 2})
        poly2 = Polynumber({(0,): 3, (1,): 2})
        assert poly1 == poly2

    def test_unequal_polynomials(self):
        """Test that different polynomials are not equal"""
        poly1 = Polynumber({(0,): 3, (1,): 2})
        poly2 = Polynumber({(0,): 3, (1,): 5})
        assert poly1 != poly2

    def test_polynomial_not_equal_to_other_type(self):
        """Test that a polynomial is not equal to another type"""
        poly = Polynumber({(0,): 3, (1,): 2})
        assert poly != 5
        assert poly != "polynomial"
        assert poly != [1, 2, 3]


class TestPolynumberAddition:
    """Test Polynumber addition operations"""

    def test_add_two_polynomials(self):
        """Test adding two polynomials"""
        poly1 = Polynumber({(0,): 3, (1,): 2})
        poly2 = Polynumber({(0,): 2, (1,): 1})
        result = poly1 + poly2
        assert result.coeffs == {(0,): 5, (1,): 3}

    def test_add_polynomials_with_different_terms(self):
        """Test adding polynomials with different terms"""
        poly1 = Polynumber({(0,): 3, (2,): 1})
        poly2 = Polynumber({(1,): 2})
        result = poly1 + poly2
        assert result.coeffs == {(0,): 3, (1,): 2, (2,): 1}

    def test_add_polynomial_to_zero(self):
        """Test adding a polynomial to zero polynomial"""
        poly1 = Polynumber({(0,): 3, (1,): 2})
        poly2 = Polynumber({})
        result = poly1 + poly2
        assert result.coeffs == {(0,): 3, (1,): 2}

    def test_reverse_add_polynomials(self):
        """Test reverse addition (radd)"""
        poly1 = Polynumber({(0,): 3, (1,): 2})
        poly2 = Polynumber({(0,): 2, (1,): 1})
        result = poly2.__radd__(poly1)
        assert result.coeffs == {(0,): 5, (1,): 3}


class TestPolynumberSubtraction:
    """Test Polynumber subtraction operations"""

    def test_subtract_two_polynomials(self):
        """Test subtracting two polynomials"""
        poly1 = Polynumber({(0,): 7, (1,): 5})
        poly2 = Polynumber({(0,): 3, (1,): 2})
        result = poly1 - poly2
        assert result.coeffs == {(0,): 4, (1,): 3}

    def test_reverse_subtract_polynomials(self):
        """Test reverse subtraction (rsub)"""
        poly1 = Polynumber({(0,): 3, (1,): 2})
        poly2 = Polynumber({(0,): 7, (1,): 5})
        result = poly1.__rsub__(poly2)
        assert result.coeffs == {(0,): 4, (1,): 3}

    def test_subtract_polynomial_from_zero(self):
        """Test subtracting a polynomial from zero polynomial"""
        zero = Polynumber({})
        poly = Polynumber({(0,): 1, (2,): 4})
        result = zero - poly
        assert result.coeffs == {(0,): -1, (2,): -4}


class TestPolynumberMultiplication:
    """Test Polynumber multiplication operations"""

    def test_multiply_polynomial_by_scalar(self):
        """Test multiplying a polynomial by a scalar"""
        poly = Polynumber({(0,): 3, (1,): 2})
        result = poly * 3
        assert result.coeffs == {(0,): 9, (1,): 6}

    def test_multiply_polynomial_by_zero(self):
        """Test multiplying a polynomial by zero"""
        poly = Polynumber({(0,): 3, (1,): 2})
        result = poly * 0
        assert result.coeffs == {}

    def test_reverse_multiply_polynomial_by_scalar(self):
        """Test reverse multiplication (rmul)"""
        poly = Polynumber({(0,): 3, (1,): 2})
        result = poly.__rmul__(3)
        assert result.coeffs == {(0,): 9, (1,): 6}

    def test_multiply_two_polynomials(self):
        """Test multiplying two polynomials"""
        poly1 = Polynumber({(1,): 2})  # 2x
        poly2 = Polynumber({(1,): 3})  # 3x
        result = poly1 * poly2
        assert result.coeffs == {(2,): 6}  # 6x^2

    def test_multiply_polynomial_binomials(self):
        """Test multiplying (x + 1) * (x + 2)"""
        poly1 = Polynumber({(0,): 1, (1,): 1})  # x + 1
        poly2 = Polynumber({(0,): 2, (1,): 1})  # x + 2
        result = poly1 * poly2
        # (x + 1)(x + 2) = x^2 + 3x + 2
        assert result.coeffs == {(0,): 2, (1,): 3, (2,): 1}

    def test_multiply_polynomial_by_negative_scalar(self):
        """Test multiplying by negative scalar"""
        poly = Polynumber({(0,): 3, (1,): 2})
        result = poly * -1
        assert result.coeffs == {(0,): -3, (1,): -2}

    def test_multiply_two_polynomials_many_coeffs(self):
        """Test multiplying two polynomials with many coefficients."""
        dim1 = randint(0, 50)
        dim2 = randint(0, 50)
        poly1_coeffs = {(d,): randint(0, 20) for d in range(dim1)}
        poly2_coeffs = {(d,): randint(0, 20) for d in range(dim2)}
        poly1 = Polynumber(poly1_coeffs)
        poly2 = Polynumber(poly2_coeffs)

        expected = {}
        for (e1,), v1 in poly1_coeffs.items():
            for (e2,), v2 in poly2_coeffs.items():
                e = (e1 + e2,)
                expected[e] = expected.get(e, 0) + (v1 * v2)
        expected = {k: v for k, v in expected.items() if v != 0}

        result = poly1 * poly2
        assert result.coeffs == expected


class TestPolynumberDivision:
    """Test Polynumber division operations"""

    def test_divide_polynomial_by_scalar(self):
        """Test dividing a polynomial by a scalar"""
        poly = Polynumber({(0,): 9, (1,): 6})
        result = poly / 3
        assert result.coeffs == {(0,): 3, (1,): 2}

    def test_divide_polynomial_by_weird_type_returns_not_implemented(self):
        """Test dividing a polynomial by a scalar"""
        poly = Polynumber({(0,): 9, (1,): 6})
        with pytest.raises(TypeError):
            poly / "hello"

    def test_divide_polynomial_by_zero_scalar_returns_not_implemented(self):
        """Test that dividing by zero returns NotImplemented"""
        poly = Polynumber({(0,): 3, (1,): 2})
        with pytest.raises(TypeError):
            poly / 0

    def test_dividing_zero_polynomial_by_scalar(self):
        """Test dividing a zero polynomial by a scalar"""
        poly = Polynumber({})
        result = poly / 5
        assert result.coeffs == {}

    def test_dividing_by_zero_polynomial_return_not_implemented(self):
         """Test that dividing by zero returns NotImplemented"""
         poly1 = Polynumber({(0,): 3, (1,): 2})
         poly2 = Polynumber({})
         with pytest.raises(TypeError):
            poly1 / poly2

    def test_dividing_zero_polynomial_by_nonzero_polynomial(self):
        poly1 = Polynumber({})
        poly2 = Polynumber({(0,): 3, (1,): 2})
        result = poly1 / poly2
        assert result.coeffs == {}

    def test_divide_negative_polynomial(self):
        poly1 = Polynumber({(0,): -9, (1,): -6})
        poly2 = Polynumber({(0,): 3, (1,): 2})
        result = poly1 / poly2
        assert result.coeffs == {(0,): -3}

    def test_dividing_large_positive_polynomials(self):
        """Test creating 2 large polynomials a,b; doing a*b=c, then checking if c/b == a & c/a == b"""
        dim1 = randint(1, 6)
        dim2 = randint(0, 6)
        poly1_coeffs = {(d,): randint(-20, 20) for d in range(dim1)}
        poly2_coeffs = {(d,): randint(-20, 20) for d in range(dim2)}
        poly1 = Polynumber(poly1_coeffs)
        poly2 = Polynumber(poly2_coeffs)
        print("poly1:", poly1)
        print("poly2:", poly2)
        poly3 = poly1 * poly2
        print("poly3:", poly3)
        assert poly3 / poly1 == poly2
        # assert poly3 / poly2 == poly1
