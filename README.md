# Symbolic-Derivative-Calculator
This project is a very simple version of a Computer Algebra System (CAS) that is fundamentally built using an Abstract Tree Structure, similar to how CAS engines like Sympy build their engines. Its features include:
- Simplifying Expressions
- Evaluating Expressions
- Computing Derivatives
- Applying Taylor Expansion
- Performing Newton's method for root approximation

# Limitations
- Unable to simplify to the most simplified form
- Evaluation of Ln(x) is accurate only for small values
- Fractional form doesn't exist, only decimals are used
- No canonical forms exist

## Example Usage

```python
from core import x, pi
from functions import Sin

expr = Sin(x) + x**2

# Differentiate
d = expr.diff(x)

# Evaluate at x = 2
value = expr.express(2, x)

# Taylor expansion around 0
taylor = expr.taylor(x, 5)


