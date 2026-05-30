from Polynumber import Polynumber
from random import randint


def setup():
    dim1 = randint(0, 5)
    dim2 = randint(0, 5)
    a = Polynumber({(d,): randint(0, 5) for d in range(dim1)})
    b = Polynumber({(d,): randint(0, 5) for d in range(dim2)})
    return a, b


def test(a, b):
    if not a.coeffs or not b.coeffs:
        print("pass -- cannot divide by 0")
        return True

    print("a", a)
    print("b", b)
    c = a * b
    print("c", c)
    print("doing c / a")
    d = c / a
    if d != b:
        print(f"fail at {c} / {a} != {b}.  == {d}")
        return False
    else:
        print("pass")
    # e = c / b
    # if e != a:
    #     print(f"fail at {c} / {b} != {a}. == {d}")
    #     return False
    # else:
    #     print("pass")
    return True


# a, b = setup()
a = Polynumber({(0,): -14, (1,): -16, (2,): 15, (3,): -9, (4,): 7, (5,): 11})
b = Polynumber({(0,): -8, (1,): -7, (2,): -7, (3,): 18, (4,): -14, (5,): 7})
test(a, b)
