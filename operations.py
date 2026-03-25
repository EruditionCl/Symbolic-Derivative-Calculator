
from core import Function
from utils import setconstant

class Binary(Function):

    """Class representing all mathematical functions
    that accept two inputs.
    
    Attributes:
        x:
            Represents first input.
        y:
            Represents second input.
    """

    def __new__(cls, x, y):
        """Creates the new object before initialization.

        This is essential as __init__ cannot return a new class
        on simplification, it must be done in __new__.
        
        Converts inputs to Constant automatically."""
        x, y=setconstant(x, y)
        obj = super().__new__(cls)
        obj.x, obj.y = x, y
        return obj.simplified()

    def __init__(self, x, y):
        pass

    def has_var(self, var):
        """Checks whether x or y has Variable var."""
        return self.x.has_var(var) or self.y.has_var(var)
    
    def __eq__(self, other):
        """Compares equality of two expressions. Returns True
        if instances are same and x and y values are equal."""
        return isinstance(other, type(self)) and self.x == other.x and self.y == other.y


class Add(Binary):

    """Class representing mathematical addition.
    Applies mathematical rules for simplifying expressions."""


    def diff(self, var):
        """Differentiates x + y with respect to var.

        f'(x+y) gives f'(x) + f'(y), hence such a result is returned."""
        return Add(self.x.diff(var), self.y.diff(var))
    
    def __str__(self):

        from functions import NaturalExp

        """Represents Add object as a string. Surrounds
        x and y with parenthesis depending on their types
        for precision."""
        left, right = f"{self.x}", f"{self.y}"
        if isinstance(self.x, (Power, Exp, NaturalExp)):
            left = f"({self.x})"
        if isinstance(self.y, (Power, Exp, NaturalExp)):
            right = f"({self.y})"
        return f"{left} + {right}"
    
    def simplified(self):

        from core import Constant, Variable
        from functions import Sin, Cos

        """Applies mathematical rules to the expression
        and simplifies it to its simplest form."""
        if self.x == 0: # 0 + y = y
            return self.y
    
        if self.y == 0: # x + 0 = x
            return self.x
        
        elif self.x == self.y: # x + x = 2x
            return Multiply(2, self.x)
        
        # Closure law. Constant + Constant = Constant.
        if all(isinstance(expr, Constant) for expr in (self.x, self.y)):
            return Constant(self.x + self.y)
        
        # Canonical sorting. Sorts x and y with priority, 
        # Constants have least priority.
        elif isinstance(self.x, Constant) and not isinstance(self.y, Constant):
            return Add(self.y, self.x)
        
        # Combines 2 variables with different coefficients to a common term.
        # A term of coefficient of 1 is considered a Variable, hence
        # a seperate rule must be introduced. 
        if isinstance(self.x, Variable) and isinstance(self.y, Multiply):
            if self.x == self.y.y:
                return Multiply(Add(1, self.y.x), self.x)
            
        # Combines 2 variables with different coefficients to a common term.
        # A term of coefficient of 1 is considered a Variable, hence
        # a seperate rule must be introduced. 
        if isinstance(self.y, Variable) and isinstance(self.x, Multiply):
            if self.y == self.x.y:
                return Multiply(Add(1, self.x.x), self.y)
            
        # Combines 2 variables with different coefficients to a common term.    
        if isinstance(self.x, Multiply) and isinstance(self.y, Multiply):
            if self.x.y == self.y.y:
                return Multiply(Add(self.x.x, self.y.x), self.x.y)
        
        # ax + (bx + c) = (a+b)x + c
        if isinstance(self.x, Multiply) and isinstance(self.y, Add):
            if isinstance(self.y.x, Multiply): 
                if self.x.y == self.y.x.y: 
                    return Add(Multiply(Add(self.x.x, self.y.x.x), self.x.y), self.y.y)
        
        # Pythagorean identity
        if isinstance(self.x, Power) and isinstance(self.x.x, Sin) and self.x.y==2:
            if isinstance(self.y, Power) and isinstance(self.y.x, Cos) and self.y.y==2:
                if self.x.x.arg==self.y.x.arg:
                    return Constant(1)
        
        # Associative Law
        if isinstance(self.x, Add):
                return Add(self.x.x, Add(self.x.y, self.y))
        return self
      
    def degree(self, var):
        if any(value == None for value in (self.x, self.y)):
            return None
        """Returns degree of the polynomial with respect to var."""
        return max(self.x.degree(var), self.y.degree(var))
    
    def express(self, variable_value, var):
        """Applies the value "variable_value" of variable "var" in an Expression."""
        return self.x.express(variable_value, var) + self.y.express(variable_value, var)


class Multiply(Binary):

    """Class representing mathematical multiplication.
    Applies mathematical rules for simplifying expressions."""

    def diff(self, var):
        """Differentiates x*y with respect to var.
        
        (xy)' = x'y + xy'"""
        return Add(Multiply(self.x.diff(var), self.y), Multiply(self.y.diff(var), self.x))

    def __str__(self):

        from core import Symbol, Identifier, Constant

        """Represents Multiply object as a string. Surrounds
        x and y with parenthesis depending on their types
        for precision."""
        if self.x == -1:
            return f"-{self.y}"
        elif self.y == -1:
            return f"-{self.x}"
        elif isinstance(self.x, Function) and isinstance(self.y, Function):
            return f"({self.x})({self.y})"
        elif isinstance(self.x, Function) and isinstance(self.y, Identifier):
            return f"{self.y}({self.x})"
        elif isinstance(self.y, Function) and isinstance(self.x, Identifier):
            return f"{self.x}({self.y})"
        elif isinstance(self.x, Constant) or isinstance(self.y, Symbol):
            return f"{self.x}{self.y}"
        elif isinstance(self.y, Constant) or isinstance(self.x, Symbol):
            return f"{self.y}{self.x}"
        return f"{self.x}{self.y}"
        
    
    def simplified(self):

        from core import Constant

        """Applies mathematical rules to the expression
        and simplifies it to its simplest form."""
        if any(value == 0 for value in (self.x, self.y)): # 0*x = 0
            return Constant(0)
        elif self.x == 1: # 1 * y = y
            return self.y
        elif self.y == 1: # x * 1 = x
            return self.x
        # Closure law. Constant * Constant = Constant.
        if all(isinstance(expr, Constant) for expr in (self.x, self.y)): 
            return Constant(self.x * self.y)
        if self.x == self.y: # x*x = x^2
            return Power(self.x, 2)
        if isinstance(self.x, Power): # x*x^n = x^(n+1)
            if self.x.x == self.y:
                return Power(self.x.x, Add(self.x.y, 1))
        if isinstance(self.y, Power): # x*x^n = x^(n+1)
            if self.y.x == self.x:
                return Power(self.y.x, Add(self.y.y, 1))
        if isinstance(self.x, Power) and isinstance(self.y, Power): # x^m * x^n = x^(m+n)
            if self.x.x == self.y.x:
                return Power(self.x.x, Add(self.x.y, self.y.y))
        if isinstance(self.x, Multiply): # Associative Law
                return Multiply(self.x.x, Multiply(self.x.y, self.y))
        return self
    
    def degree(self, var):
        if any(value == None for value in (self.x, self.y)):
            return None
        """Returns the degree of the polynomial with respect to var."""
        return self.x.degree(var) + self.y.degree(var)
    
    def express(self, x, var):
        """Applies the value "variable_value" of variable "var" in an Expression."""
        return self.x.express(x, var) * self.y.express(x, var)


class Subtract(Binary):
    """Automatically converts instance into Add(x, -y)."""
    def __new__(cls, x, y):
        x, y=setconstant(x, y)
        return x + -y


class Divide(Binary):
    """Automatically converts instance into Multiply(x, y**-1)."""
    def __new__(cls, x, y):
        x, y=setconstant(x, y)
        return x * y ** -1
    

class Power(Binary):

    """Class representing mathematical power functions.
    Applies mathematical rules for simplifying expressions."""

    def simplified(self):

        from core import Constant, e
        from functions import NaturalExp

        """Applies mathematical rules to the expression
        and simplifies it to its simplest form."""

        if all(isinstance(value, Constant) for value in (self.x, self.y)):
            return Constant(self.x ** self.y)
        if self.y == 0:
            return Constant(1)
        elif self.y == 1:
            return self.x
        if isinstance(self.x, Power):
            return Power(self.x.x, Multiply(self.x.y, self.y))
        if self.x == e:
            return NaturalExp(self.y)
        if self.y.has_var(None):
            return Exp(self.x, self.y)
        return self
    
    def diff(self, var): 
        """Differentiates x**y with respect to var.
        
        (x ** y)' = x' * (x ^ (y-1)) * y"""
        return Multiply(Multiply(self.y, Power(self.x, Subtract(self.y, 1))), self.x.diff(var))

    def __str__(self):
        """Represents Power object as a string. Surrounds
        x and y with parenthesis depending on their types
        for precision."""
        if isinstance(self.x, Function) and isinstance(self.y, Function):   
            return f"({self.x}) ^ ({self.y})"    
        if isinstance(self.x, Function):
            return f"({self.x}) ^ {self.y}"
        if isinstance(self.y, Function):
            return f"{self.x} ^ ({self.y})"
        return f"{self.x} ^ {self.y}"
    
    def degree(self,var):

        from core import Constant

        """Returns the degree of the polynomial with respect to var."""
        if any(value == None for value in (self.x.degree(var), self.y.degree(var))):
            return None
        elif isinstance(self.y, Constant):
            return self.x.degree(var) * self.y.value    
        return 0   
        
    def express(self, x, var):
        """Applies the value "variable_value" of variable "var" in an Expression."""
        return self.x.express(x, var) ** self.y.express(x, var)


class Exp(Binary):

    """Class representing the mathematical exponential function.
    Applies mathematical rules for simplifying expressions."""

    def degree(self, var):
        """Returns the degree of the polynomial with respect to var.
        
        If var is in the exponent, it is not a polynomial hence return None."""
        if self.y.has_var(var):
            return None
        return 0
    
    def express(self, variable_value, var):
        """Applies the value "variable_value" of variable "var" in an Expression."""
        return self.x.express(variable_value, var) ** self.y.express(variable_value, var)

    def simplified(self):

        from core import Constant, e, valuetypes
        from functions import NaturalExp

        """Applies mathematical rules to the expression
        and simplifies it to its simplest form."""

        if self.x == 1: # 1 ** x = 1
            return Constant(1)
        elif self.x == 0: # 0 ** x = 0
            if self.y < 0:
                raise ZeroDivisionError("0 to the power of negative is undefined.")
            return Constant(0)
        elif self.x == e: 
            return NaturalExp(self.y)
        if isinstance(self.y, valuetypes): # a ** Constant is a Power function.
            return Power(self.x, self.y)
        return self

    def diff(self,var):

        from functions import Ln

        """Differentiates Exp object with respect to var.
        
        (a^x)' = a^x * (x'ln(a) + x * a'/a) """
        return self * ((self.y.diff(var) * Ln(self.x)) + self.y * (self.x.diff(var) / self.x))
    
    def __str__(self):
        """Represents Power object as a string. Surrounds
        x and y with parenthesis depending on their types
        for precision."""
        if isinstance(self.x, Function) and isinstance(self.y, Function):   
            return f"({self.x}) ^ ({self.y})"    
        if isinstance(self.x, Function):
            return f"({self.x}) ^ {self.y}"
        if isinstance(self.y, Function):
            return f"{self.x} ^ ({self.y})"
        return f"{self.x} ^ {self.y}"