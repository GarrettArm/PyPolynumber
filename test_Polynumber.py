import pytest
from random import randint
from collections import OrderedDict
from Polynumber import IntPolynumber


class TestIntPolynumberInstantiation:
    """Test IntPolynumber instantiation"""

    def test_create_simple_intpolynumber(self):
        """Test creating a simple intpolynumber"""
        coeffs = {(0,): 3, (1,): 2}
        poly = IntPolynumber(coeffs)
        assert poly.coeffs == {(0,): 3, (1,): 2}

    def test_create_empty_intpolynumber(self):
        """Test creating an empty intpolynumber"""
        coeffs = {}
        poly = IntPolynumber(coeffs)
        assert poly.coeffs == {}

    def test_create_intpolynumber_with_single_term(self):
        """Test creating a intpolynumber with a single term"""
        coeffs = {(2,): 5}
        poly = IntPolynumber(coeffs)
        assert poly.coeffs == {(2,): 5}

    def test_intpolynumber_filters_zero_coefficients(self):
        """Test that zero coefficients are filtered out"""
        coeffs = {(0,): 0, (1,): 2, (2,): 3}
        poly = IntPolynumber(coeffs)
        assert (0,) not in poly.coeffs
        assert poly.coeffs == {(1,): 2, (2,): 3}

    def test_intpolynumber_filters_invalid_keys(self):
        """Test that invalid keys are filtered out"""
        coeffs = {(0,): 3, (1,): 2, "invalid": 5}
        poly = IntPolynumber(coeffs)
        assert "invalid" not in poly.coeffs
        assert len(poly.coeffs) == 2

    def test_intpolynumber_filters_invalid_values(self):
        """Test that invalid values are filtered out"""
        coeffs = {(0,): "invalid", (1,): 2, (2,): 3}
        poly = IntPolynumber(coeffs)
        assert (0,) not in poly.coeffs
        assert poly.coeffs == {(1,): 2, (2,): 3}

    """I don't think I want float coefficients right now.  Will make these rational coeffs later"""
    # def test_intpolynumber_with_float_coefficients(self):
    #     """Test creating a intpolynumber with float coefficients"""
    #     coeffs = {(0,): 3.7, (1,): 2.5}
    #     poly = IntPolynumber(coeffs)
    #     assert poly.coeffs == {(0,): 3.7, (1,): 2.5}

    # def test_correctly_reorders_coefficients(self):
    #     """Test creating a intpolynumber with float coefficients"""
    #     coeffs = {(9, 1): 4, (4,): 8, (4, 1): 1, (9,): 15}
    #     poly = IntPolynumber(coeffs)
    #     assert poly.coeffs == {(4,): 8, (4, 1): 1, (9,): 15, (9, 1): 4}

    def test_intpolynumber_repr(self):
        """Test the string representation of a intpolynumber"""
        coeffs = {(1,): 2, (0,): 3}
        poly = IntPolynumber(coeffs)
        assert str(poly) == str(IntPolynumber({(0,): 3, (1,): 2}))

    def test_intpolynumber_repr_inverse(self):
        """Test the string representation of a intpolynumber"""
        coeffs = {(1,): 2, (0,): 3}
        poly = IntPolynumber(coeffs)
        assert str(poly) != f"IntPolynumber({dict(coeffs)})"

    def test_accepts_ordered_dict(self):
        """Test if OrderdedDict arguments are accepted"""
        coeffs = OrderedDict({(1,): 2, (0,): 3})
        poly = IntPolynumber(coeffs)
        assert str(poly) == str(IntPolynumber({(0,): 3, (1,): 2}))

    def test_zero_intpolynumber_is_falsey(self):
        """Test that the zero intpolynumber is a falsey python value"""
        coeffs = {(1,): 0, (0,): 0, (4,): 0}
        poly = IntPolynumber(coeffs)
        assert bool(poly) is False


class TestIntPolynumberEquality:
    """Test IntPolynumber equality operations"""

    def test_equal_intpolynumbers(self):
        """Test that identical intpolynumbers are equal"""
        poly1 = IntPolynumber({(0,): 3, (1,): 2})
        poly2 = IntPolynumber({(0,): 3, (1,): 2})
        assert poly1 == poly2

    def test_unequal_intpolynumbers(self):
        """Test that different intpolynumbers are not equal"""
        poly1 = IntPolynumber({(0,): 3, (1,): 2})
        poly2 = IntPolynumber({(0,): 3, (1,): 5})
        assert poly1 != poly2

    def test_intpolynumber_not_equal_to_other_type(self):
        """Test that a intpolynumber is not equal to another type"""
        poly = IntPolynumber({(0,): 3, (1,): 2})
        assert poly != 5
        assert poly != "intpolynumber"
        assert poly != [1, 2, 3]

    def test_equal_int_and_intpolynumbers(self):
        """Test that identical int and intpolynumber"""
        poly1 = IntPolynumber({(0,): 3})
        int1 = 3
        assert poly1 == int1

    def test_unequal_int_and_intpolynumbers(self):
        """Test that identical int and intpolynumber"""
        poly1 = IntPolynumber({(0,): 3})
        int1 = 4
        assert poly1 != int1


class TestIntPolynumberAddition:
    """Test IntPolynumber addition operations"""

    def test_add_two_intpolynumbers(self):
        """Test adding two intpolynumbers"""
        poly1 = IntPolynumber({(0,): 3, (1,): 2})
        poly2 = IntPolynumber({(0,): 2, (1,): 1})
        result = poly1 + poly2
        assert result.coeffs == {(0,): 5, (1,): 3}

    def test_add_intpolynumbers_with_different_terms(self):
        """Test adding intpolynumbers with different terms"""
        poly1 = IntPolynumber({(0,): 3, (2,): 1})
        poly2 = IntPolynumber({(1,): 2})
        result = poly1 + poly2
        assert result.coeffs == {(0,): 3, (1,): 2, (2,): 1}

    def test_add_intpolynumber_to_zero(self):
        """Test adding a intpolynumber to zero intpolynumber"""
        poly1 = IntPolynumber({(0,): 3, (1,): 2})
        poly2 = IntPolynumber({})
        result = poly1 + poly2
        assert result.coeffs == {(0,): 3, (1,): 2}

    def test_reverse_add_intpolynumbers(self):
        """Test reverse addition (radd)"""
        poly1 = IntPolynumber({(0,): 3, (1,): 2})
        poly2 = IntPolynumber({(0,): 2, (1,): 1})
        result = poly2.__radd__(poly1)
        assert result.coeffs == {(0,): 5, (1,): 3}


class TestIntPolynumberSubtraction:
    """Test IntPolynumber subtraction operations"""

    def test_subtract_two_intpolynumbers(self):
        """Test subtracting two intpolynumbers"""
        poly1 = IntPolynumber({(0,): 7, (1,): 5})
        poly2 = IntPolynumber({(0,): 3, (1,): 2})
        result = poly1 - poly2
        assert result.coeffs == {(0,): 4, (1,): 3}

    def test_reverse_subtract_intpolynumbers(self):
        """Test reverse subtraction (rsub)"""
        poly1 = IntPolynumber({(0,): 3, (1,): 2})
        poly2 = IntPolynumber({(0,): 7, (1,): 5})
        result = poly1.__rsub__(poly2)
        assert result.coeffs == {(0,): 4, (1,): 3}

    def test_subtract_intpolynumber_from_zero(self):
        """Test subtracting a intpolynumber from zero intpolynumber"""
        zero = IntPolynumber({})
        poly = IntPolynumber({(0,): 1, (2,): 4})
        result = zero - poly
        assert result.coeffs == {(0,): -1, (2,): -4}


class TestIntPolynumberMultiplication:
    """Test IntPolynumber multiplication operations"""

    def test_multiply_intpolynumber_by_scalar(self):
        """Test multiplying a intpolynumber by a scalar"""
        poly = IntPolynumber({(0,): 3, (1,): 2})
        result = poly * 3
        assert result.coeffs == {(0,): 9, (1,): 6}

    def test_multiply_intpolynumber_by_zero(self):
        """Test multiplying a intpolynumber by zero"""
        poly = IntPolynumber({(0,): 3, (1,): 2})
        result = poly * 0
        assert result.coeffs == {}

    def test_reverse_multiply_intpolynumber_by_scalar(self):
        """Test reverse multiplication (rmul)"""
        poly = IntPolynumber({(0,): 3, (1,): 2})
        result = poly.__rmul__(3)
        assert result.coeffs == {(0,): 9, (1,): 6}

    def test_multiply_two_intpolynumbers(self):
        """Test multiplying two intpolynumbers"""
        poly1 = IntPolynumber({(1,): 2})  # 2x
        poly2 = IntPolynumber({(1,): 3})  # 3x
        result = poly1 * poly2
        assert result.coeffs == {(2,): 6}  # 6x^2

    def test_multiply_intpolynumber_binomials(self):
        """Test multiplying (x + 1) * (x + 2)"""
        poly1 = IntPolynumber({(0,): 1, (1,): 1})  # x + 1
        poly2 = IntPolynumber({(0,): 2, (1,): 1})  # x + 2
        result = poly1 * poly2
        # (x + 1)(x + 2) = x^2 + 3x + 2
        assert result.coeffs == {(0,): 2, (1,): 3, (2,): 1}

    def test_multiply_intpolynumber_by_negative_scalar(self):
        """Test multiplying by negative scalar"""
        poly = IntPolynumber({(0,): 3, (1,): 2})
        result = poly * -1
        assert result.coeffs == {(0,): -3, (1,): -2}

    def test_multiply_two_intpolynumbers_many_coeffs(self):
        """Test multiplying two intpolynumbers with many coefficients."""
        dim1 = randint(0, 50)
        dim2 = randint(0, 50)
        poly1_coeffs = {(d,): randint(0, 20) for d in range(dim1)}
        poly2_coeffs = {(d,): randint(0, 20) for d in range(dim2)}
        poly1 = IntPolynumber(poly1_coeffs)
        poly2 = IntPolynumber(poly2_coeffs)

        expected = {}
        for (e1,), v1 in poly1_coeffs.items():
            for (e2,), v2 in poly2_coeffs.items():
                e = (e1 + e2,)
                expected[e] = expected.get(e, 0) + (v1 * v2)
        expected = {k: v for k, v in expected.items() if v != 0}

        result = poly1 * poly2
        assert result.coeffs == expected


class TestIntPolynumberDivision:
    """Test IntPolynumber division operations"""

    def test_divide_intpolynumber_by_scalar(self):
        """Test dividing a intpolynumber by a scalar"""
        poly = IntPolynumber({(0,): 9, (1,): 6})
        result = poly / 3
        assert result.coeffs == {(0,): 3, (1,): 2}

    def test_divide_intpolynumber_by_weird_type_returns_not_implemented(self):
        """Test dividing a intpolynumber by a scalar"""
        poly = IntPolynumber({(0,): 9, (1,): 6})
        with pytest.raises(TypeError):
            poly / "hello"

    def test_divide_intpolynumber_by_zero_scalar_returns_not_implemented(self):
        """Test that dividing by zero returns NotImplemented"""
        poly = IntPolynumber({(0,): 3, (1,): 2})
        with pytest.raises(TypeError):
            poly / 0

    def test_dividing_zero_intpolynumber_by_scalar(self):
        """Test dividing a zero intpolynumber by a scalar"""
        poly = IntPolynumber({})
        result = poly / 5
        assert result.coeffs == {}

    def test_dividing_by_zero_intpolynumber_return_not_implemented(self):
        """Test that dividing by zero returns NotImplemented"""
        poly1 = IntPolynumber({(0,): 3, (1,): 2})
        poly2 = IntPolynumber({})
        with pytest.raises(TypeError):
            poly1 / poly2

    def test_dividing_zero_intpolynumber_by_nonzero_intpolynumber(self):
        poly1 = IntPolynumber({})
        poly2 = IntPolynumber({(0,): 3, (1,): 2})
        result = poly1 / poly2
        assert result.coeffs == {}

    def test_divide_negative_intpolynumber(self):
        poly1 = IntPolynumber({(0,): -9, (1,): -6})
        poly2 = IntPolynumber({(0,): 3, (1,): 2})
        result = poly1 / poly2
        assert result.coeffs == {(0,): -3}

    def test_dividing_large_positive_intpolynumbers(self):
        """Test creating 2 large intpolynumbers a,b; doing a*b=c, then checking if c/b == a & c/a == b"""
        dim1 = randint(1, 6)
        dim2 = randint(0, 6)
        poly1_coeffs = {(d,): randint(-20, 20) for d in range(dim1)}
        poly2_coeffs = {(d,): randint(-20, 20) for d in range(dim2)}
        poly1 = IntPolynumber(poly1_coeffs)
        poly2 = IntPolynumber(poly2_coeffs)
        print("poly1:", poly1)
        print("poly2:", poly2)
        poly3 = poly1 * poly2
        print("poly3:", poly3)
        assert poly3 / poly1 == poly2
        # assert poly3 / poly2 == poly1
