
import unittest
from calculator import *

class TestSymbolicDerivativeCalculator(unittest.TestCase):

    def setUp(self):
        self.x = Variable('x')
        self.y = Variable('y')
        self.c = Constant(5)
        self.zero = Constant(0)
        self.one = Constant(1)

    def test_constant_creation(self):
        c1 = Constant(3.14)
        self.assertEqual(c1.value, 3.14)
        c2 = Constant(c1)
        self.assertEqual(c2.value, 3.14)

    def test_constant_operations(self):
        c1 = Constant(10)
        c2 = Constant(3)
        self.assertEqual((c1 + c2).value, 13)
        self.assertEqual((c1 - c2).value, 7)
        self.assertEqual((c1 * c2).value, 30)
        self.assertEqual((c1 / c2).value, 10/3)

    def test_variable_creation(self):
        x = Variable('x')
        self.assertEqual(x.symbol, 'x')
        y = Variable('y')
        self.assertNotEqual(x, y)

    def test_variable_derivative(self):
        self.assertEqual(self.x.diff(self.x), self.one)
        self.assertEqual(self.x.diff(self.y), self.zero)
        self.assertEqual(self.y.diff(self.y), self.one)

    def test_constant_derivative(self):
        self.assertEqual(self.c.diff(self.x), self.zero)
        self.assertEqual(self.zero.diff(self.x), self.zero)

    def test_add_derivative(self):
        expr = self.x + self.c
        self.assertEqual(expr.diff(self.x), self.one)

        expr2 = self.x + self.y
        self.assertEqual(expr2.diff(self.x), self.one)

    def test_subtract_derivative(self):
        expr = self.x - self.c
        self.assertEqual(expr.diff(self.x), self.one)

        expr2 = self.x - self.y
        self.assertEqual(expr2.diff(self.x), self.one)

    def test_multiply_derivative(self):
        expr = self.x * self.c
        self.assertEqual(expr.diff(self.x), self.c)

        expr2 = self.x * self.y
        self.assertEqual(expr2.diff(self.x), self.y)

    def test_power_derivative(self):
        expr = self.x ** Constant(2)
        expected = Constant(2) * self.x
        self.assertEqual(expr.diff(self.x), expected)

        expr2 = self.x ** Constant(3)
        expected2 = Constant(3) * (self.x ** Constant(2))
        self.assertEqual(expr2.diff(self.x), expected2)

    def test_sin_derivative(self):
        expr = Sin(self.x)
        expected = Cos(self.x)
        self.assertEqual(expr.diff(self.x), expected)

    def test_cos_derivative(self):
        expr = Cos(self.x)
        expected = Constant(-1) * Sin(self.x)
        self.assertEqual(expr.diff(self.x), expected)

    def test_tan_derivative(self):
        expr = Tan(self.x)
        expected = Constant(1) / (Cos(self.x) ** Constant(2))
        self.assertEqual(expr.diff(self.x), expected)

    def test_ln_derivative(self):
        expr = Ln(self.x)
        expected = Constant(1) / self.x
        self.assertEqual(expr.diff(self.x), expected)

    def test_exp_derivative(self):
        expr = NaturalExp(self.x)
        expected = NaturalExp(self.x)
        self.assertEqual(expr.diff(self.x), expected)

    def test_chain_rule(self):
        expr = Sin(self.x ** Constant(2))
        expected = Cos(self.x ** Constant(2)) * (Constant(2) * self.x)
        self.assertEqual(expr.diff(self.x), expected)

        expr2 = Ln(self.x ** Constant(2))
        expected2 = expr2.diff(self.x)
        self.assertEqual(expr2.diff(self.x), expected2)

    def test_product_rule(self):
        expr = self.x * Sin(self.x)
        expected = expr.diff(self.x)
        self.assertEqual(expr.diff(self.x), expected)

    def test_quotient_rule(self):
        expr = Sin(self.x) / self.x
        expected = expr.diff(self.x)
        self.assertEqual(expr.diff(self.x), expected)

    def test_orderdiff(self):
        expr = self.x ** Constant(3)
        first = expr.orderdiff(self.x, 1)
        expected_first = Constant(3) * (self.x ** Constant(2))
        self.assertEqual(first, expected_first)

        third = expr.orderdiff(self.x, 3)
        expected_third = Constant(6)
        self.assertEqual(third, expected_third)

    def test_taylor_series(self):
        expr = Sin(self.x)
        taylor = expr.taylor(self.x, 3, 0)
        expected = taylor
        self.assertEqual(taylor, expected)

    def test_expression_evaluation(self):
        expr = self.x ** Constant(2) + Constant(3)
        result = expr.express(2, self.x)
        self.assertEqual(result, Constant(7))

        result2 = expr.express(0, self.x)
        self.assertEqual(result2, Constant(3))

    def test_newtons_method(self):
        expr = self.x ** Constant(2) - Constant(2)
        root = expr.newtons_method(2, self.x, 5)
        expected = Constant(1.4142135623730951)
        self.assertAlmostEqual(root, expected, places=5)

    def test_polynomial_degree(self):
        expr = self.x ** Constant(3) + self.x ** Constant(2) + self.x + Constant(1)
        self.assertEqual(expr.degree(self.x), 3)

        expr2 = Constant(5)
        self.assertEqual(expr2.degree(self.x), 0)

        expr3 = self.x * self.y
        self.assertEqual(expr3.degree(self.x), 1)

    def test_has_var(self):
        expr = self.x ** Constant(2) + Sin(self.y)
        self.assertTrue(expr.has_var(self.x))
        self.assertTrue(expr.has_var(self.y))
        self.assertFalse(expr.has_var(Variable('z')))

        expr2 = Constant(5)
        self.assertFalse(expr2.has_var(self.x))

if __name__ == '__main__':
    unittest.main()

