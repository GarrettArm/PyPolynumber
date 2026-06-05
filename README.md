# PyPolynumber
- chose to represent this as {(a,b,...): c}
- an alternative was to use a grid of slots:

|    |    |    |    |   |
|----|----|----|----|---|
|x<sup>0</sup>y<sup>0</sup>|x<sup>1</sup>y<sup>0</sup>|x<sup>2</sup>y<sup>0</sup>|x<sup>3</sup>y<sup>0</sup>|...|
|x<sup>0</sup>y<sup>1</sup>|x<sup>1</sup>y<sup>1</sup>|x<sup>2</sup>y<sup>1</sup>|...|
|x<sup>0</sup>y<sup>2</sup>|... 

with c being the value in each slot


__Some Polynumber__ types to encode polynomial expressions.
- represented as {(a,b,...): c, ...}
    - {(0,): 5, (1,): 4, (2,): 3} ==> 3x^2 + 4x^1 + 5x^0
    - {(0,1,): 5, (2,1,): 3} ==> 3x^2y^1 + 5x^0y^1
- has overloaded +, -, *, **, /, etc for behavior specific to these types
- can be evaluated at some x by calling the mypolynum(x)


__An IntPolynumber__ only allow integers in the coefficients & exponents
- i.e., 2x^4 + 3x + 7
- it supports +, -, *, /, **
- it can be evaluated a some x value by calling the Polynumber(x)


__A FractionPolynumber__ only allows integer fractions in the coefficients & exponents
- i.e.,  (3/2)x^(4/1) + (4/1)x^(1/2) + (7/1)
- it supports +, -, *, and **, but not / at the moment


__A RationalPolynumber__ is a fraction with Polynumbers as an Numerator / Denominator.


Following Norman Wildberger's discussion of the topic.
