# Symbolic-Derivative-Calculator
This project is a very simple version of a Computer Algebra System (CAS) that is fundamentally built using an Abstract Tree Structure, similar to how CAS engines like Sympy build their engines. Its features include:
- Simplifying Expressions
- Evaluating Expressions
- Computing Derivatives
- Applying Taylor Expansion
- Performing Newton's method for root approximation

# Working Principle
When a mathematical expression is written, the program translates the expression into an Abstract Syntax Tree. That means, Each expression is converted into trees, with nodes being the inputs and the branches being the operator. 

         2xy
         / \
        / * \
       2x    y
      / \
     / * \
    2     x
In this example, it splits 2xy into 2x and y, and further splits 2x into 2 and x. Then if we want to take the derivative, it applies the derivative rules to the bottom most elements of the tree and works its way up. 
# Limitations
- Unable to simplify to the most simplified form
- Evaluation of Ln(x) is accurate only for small values
- Fractional form doesn't exist, only decimals are used
- No canonical forms exist

## Example Usage

```python
from core import *
from functions import *
from operations import *

expr = Sin(x) + x**2

# Differentiate
d = expr.diff(x)

# Evaluate at x = 2
value = expr.express(2, x)

# Taylor expansion around 0
taylor = expr.taylor(x, 5)


