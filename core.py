
class Expression:
    """The base class from which all mathematical functions
        and symbols are built and inherited from.
    
    Supports standard operations via operator overloading.

    Direct Subclasses include Identifier and Function

    """
    
    def __init__(self):
        pass
    
    def __add__(self, other):
        from operations import Add
        return Add(self, other)
    
    def __radd__(self, other):
        from operations import Add
        return Add(other, self)

    def __sub__(self, other):
        from operations import Subtract
        return Subtract(self, other)
    
    def __rsub__(self, other):
        from operations import Subtract
        return Subtract(other, self)

    def __mul__(self, other):
        from operations import Multiply
        return Multiply(self, other)
    
    def __rmul__(self, other):
        from operations import Multiply
        return Multiply(other, self)
    
    def __truediv__(self, other):
        from operations import Divide
        return Divide(self, other)
    
    def __rtruediv__(self, other):
        from operations import Divide
        return Divide(other, self)
    
    def __pow__(self, other):
        from operations import Power
        return Power(self, other)

    def __rpow__(self, other):
        from operations import Power
        return Power(other, self)
    
    def __neg__(self):
        from operations import Multiply
        return Multiply(-1, self)

    def __pos__(self):
        return self
    
    def orderdiff(self, var, n=1):
        """Computes the nth order derivative with respect to a variable.
        
        Args:
            var: Variable to differentiate with respect to.
            n: nth order of derivative. default is 1.

        Returns:
            Expression: Result after differentiating n times

        """
        for _ in range(n):
            self = self.diff(var)
        return self

    def taylor(self, var, n=10, a=0):

        from utils import factorial

        """Converts an expression to a taylor expansion.
        
        Args:
            var: Which variable to be expanded with respect to
                
            n: Number of terms of expansion. Default is 10.
                
            a: Central point of expansion. Default is 0.
                
        Returns:
            result: Taylor series of the expression with n terms

        """
        result = 0
        for i in range(n+1):

            func = self.orderdiff(var, i)
            func_express = func.express(a, var)
            polynomial = (var - a) ** i

            result = (func_express * polynomial) / factorial(i) + result

        return result
    
    def newtons_method(self, first_approx, var, iterations=5):
        """Applies Newton's Method to Expression and approximates x-intercept.

        Args:
            first_approx: First approximation to begin.
            var: Variable the method is to be applied to.
            iterations: Number of times method is applied.

        Returns:
            Final approximation of x-intercept.
        
        """
        f_x = self.express(first_approx, var)
        f_prime_x = self.diff(var).express(first_approx, var)

        next_iteration = first_approx - (f_x) / (f_prime_x)

        for _ in range(iterations-1):

            f_x = self.express(next_iteration, var)
            f_prime_x = self.diff(var).express(next_iteration, var)

            next_iteration = next_iteration - (f_x)/(f_prime_x)

        return next_iteration


class Identifier(Expression):
    """The class mathematical symbols and values inherit from.
    
    Class is intended to be subclassed by Value and Variable."""
    def __init__(self):
        pass


class Value(Identifier): 
    """Class used to define real numbers. 
    
    Class is intended to be subclassed by Constant and Symbol.
    """

    def __init__(self):
        pass

    def diff(self, var):
        """Returns the derivative of a constant, zero."""
        return Constant(0)
    
    def simplified(self):
        """Constants are already in their simplest forms, hence returns self"""
        return self
    
    def express(self, variable_value, var):
        """Constants evaluate to themselves, hence returns self"""
        return self
    
    def degree(self, var):
        """Polynomials consist of variables, not constants, hence returns 0."""
        return 0
    
    def has_var(self, var):
        """Constants consist of real numbers, not variables, hence False,"""
        return False
    
    def __gt__(self, other):
        """Return True if self.value > other (or other.value)."""
        if isinstance(other, (int, float)):
            return self.value > other
        return self.value > other.value
    
    def __lt__(self, other):
        """Return True if self.value < other (or other.value)."""
        if isinstance(other, (int, float)):
            return self.value < other
        return self.value < other.value
    
    def __ge__(self, other):
        """Return True if self.value >= other (or other.value)."""
        if isinstance(other, (int, float)):
            return self.value >= other
        return self.value >= other.value
    
    def __le__(self, other):
        """Return True if self.value <= other (or other.value)."""
        if isinstance(other, (int, float)):
            return self.value <= other
        return self.value <= other.value
    
    def __mod__(self, other):
        """Returns self.value modulu other (or other.value)"""
        if isinstance(other, (int, float)):
            return Constant(self.value % other)
        return Constant(self.value % other.value)


class Constant(Value):
    """Class consisting of all real numbers that are not special mathematical constants
    
    Attributes:
        value: Represents the numerical value of the instance."""

    def __init__(self, value):
        """Creates instance from a number or another Constant.

        Args:
            value (int, float, Constant): Numerical value to be represented
            
        Raise:
            Raises ValueError if input is not Constant, float or int"""
        
        if isinstance(value, Constant):
            value = value.value
        elif not any(isinstance(value, category) for category in valuetypes):
            raise ValueError("Constant only accepts float, int or Constant")
        self.value=value 
    
    def __str__(self):
        return f"{self.value}"
    
    def __eq__(self, other): 
        """Return True if self.value == other (or other.value)."""
        if isinstance(other, Constant):
            return self.value == other.value
        elif isinstance(other, (int, float)):
            return self.value == other
        return False
    
    def __add__(self, other):
        
        from operations import Add

        """Return Sum of self.value and other (or other.value)"""
        if isinstance(other, (int, float)):
            return Constant(self.value + other)
        elif isinstance(other, Constant):
            return Constant(self.value + other.value)
        return Add(self, other)
    
    def __sub__(self, other):

        from operations import Subtract

        """Return Difference of self.value and other (or other.value)"""
        if isinstance(other, (int, float)):
            return Constant(self.value - other)
        elif isinstance(other, Constant):
            return Constant(self.value - other.value)
        return Subtract(self, other)

    def __mul__(self, other):

        from operations import Multiply

        """Return Product of self.value and other (or other.value)"""
        if isinstance(other, (int, float)):
            return Constant(self.value * other)
        elif isinstance(other, Constant):
            return Constant(self.value*  other.value)
        return Multiply(self, other)
    
    def __rmul__(self, other):
        """Return Product of other (or other.value) and self.value"""
        return self.__mul__(other)
    
    def __truediv__(self, other):

        from operations import Divide

        """Return Quotient of self.value and other (or other.value)"""
        if isinstance(other, (int, float)):
            return Constant(self.value / other)
        elif isinstance(other, Constant):
            return Constant(self.value / other.value)
        return Divide(self, other)
    
    def __pow__(self, other):

        from operations import Power

        """Return the result of Exponention of self.value and other (or other.value)"""
        if isinstance(other, (int, float)):
            return Constant(self.value ** other)
        elif isinstance(other, Constant):
            return Constant(self.value ** other.value)
        return Power(self, other)
    
    def __round__(self, ndigits=10):
        """Rounds number to ndigits digits of accuracy. Default is 10."""
        return round(self.value, ndigits)


class Variable(Identifier):

    """Class representing all mathematical quantities that can vary.
    
    Attributes:
        symbol:
            Represents symbol for unknown value (eg: x)."""

    def __init__(self, symbol):
        self.symbol = symbol

    def diff(self, var):
        """Differentiating a variable with respect to itself returns 1."""
        if var == self:
            return Constant(1)
    # Assumes all derivatives are partial derivatives,
    # So if a variable is differentiated with respect to another variable,
    # It is assumed that this variable is a constant.
        else:
            return Constant(0) 


    def degree(self, var):
        """Polynomial of a single variable is to the power of 1.
        Assumes multiple variables, so if variables
        don't match, returns self."""
        if self == var:
            return 1
        return 0

    def express(self, variable_value, var):
        """Expresses the value of a variable. Assumes multiple variables.
        So if variables dont match, returns self."""
        if var == self:
            return Constant(variable_value)
        return self
    
    def has_var(self, var):
        """Checks if a specific variable is present.
        If var==None, looks for any variable."""
        if var == None:
            return True
        return self == var
        
    def __str__(self):
        return f"{self.symbol}" 
    
    def __eq__(self, other):
        return isinstance(other, Variable) and self.symbol == other.symbol
    
class Function(Expression):

    """Represents the class for all mathematical functions.

    Class is intended to be subclassed by Unary and Binary."""

    def __init__(self):
        pass

class Symbol(Value):
    """Class consisting of special mathematical constants"""
    
    def __init__(self):
        pass

    def __eq__(self, other):
        return isinstance(other, type(self))


class Euler(Symbol):

    """Class representing Euler's number e.
    
    Attributes:
        value:
            Equal to value of e."""

    def __init__(self):
        self.value=2.718281828459045
        super().__init__()
    
    def __str__(self):
        return "e"


class Pi(Symbol):

    """Class representing π.
    
    Attributes:
        value:
            Equal to the value of π."""

    def __init__(self):
        self.value=3.14159265358979
        super().__init__()
    
    def __str__(self):
        return "π"
    

e=Euler()
pi=Pi()
π=pi
valuetypes = (int, float, Constant)
x=Variable("x") 
y=Variable("y")
z=Variable("z")