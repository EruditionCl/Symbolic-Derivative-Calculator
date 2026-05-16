# Symbolic-Derivative-Calculator
This project is a very simple version of a Computer Algebra System (CAS) that is fundamentally built using an Abstract Tree Structure, similar to how CAS engines like Sympy build their engines, but built entirely from native Python without any dependencies. Its features include:

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

Recursive symbolic differentiation is also utilized. Derivatives of most functions are defined as $f \prime (g(x)) \cdot g \prime (x)$ which makes differentiation as a traversal through an expression tree. For example, derivative of $sin(x)$ is defined as $cos(x) \cdot x \prime$ hence pre computer formulas for each case is not required.
# Limitations
- Unable to simplify to the most mathematically simple form
- Evaluation of Ln(x) is accurate only for small values
- Fractional form doesn't exist, Floating point arithmetic
- No canonical forms exist

## Example Usage

```python
from calculator import *

expr = Sin(x) + x**2

# Differentiate
d = expr.diff(x)

# Evaluate at x = 2
value = expr.express(2, x)

# Taylor expansion around 0
taylor = expr.taylor(x, 5)


