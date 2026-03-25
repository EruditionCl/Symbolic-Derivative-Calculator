
from core import Function

class Unary(Function):

    """Class representing all mathematical functions
    that accept only one input.
    
    Attributes:
        arg:
            Represents the single input.
        evaluate:
            Represents whether to evaluate the unary
            and convert it to a constant.
    """

    evaluate=False

    @classmethod
    def evaluatefunc(cls, input):
        """Function to allow evaluation of a unary to a constant."""
        cls.evaluate = input

    def __new__(cls, arg):

        from utils import setconstant

        """Creates the new object before initialization.

        This is essential as __init__ cannot return a new class
        on simplification, it must be done in __new__.
        
        Converts inputs to Constant automatically."""
        arg, = setconstant(arg)
        obj = super().__new__(cls)
        obj.arg = arg
        return obj.simplified()

    def __init__(self, arg):
        pass
    
    def has_var(self, var):
        """Checks whether instance variable arg has Variable var."""
        return self.arg.has_var(var)
    
    def degree(self, var):
        """Returns degree of the polynomial. 
        
        Checks whether a variable is present in the arg.
        If a variable is in a transcedental function, 
        it is not considered a polynomial. Hence return None.
        
        Otherwise the arg is a Constant and hence the degree is 0."""
        if self.arg.has_var(var):
            return None
        return 0
    
    def express(self, variable_value, var):
        """Expresses the argument of the unary with a value."""
        return type(self)((self.arg.express(variable_value, var)))

    def __eq__(self, other):
        """Compares equality of two expressions. Returns True
        if instances are same and arg values are equal."""
        return isinstance(other, type(self)) and self.arg == other.arg



class Sin(Unary):

    """Class representing mathematical Sine function.
    Applies mathematical rules for simplifying expressions."""

    def simplified(self):

        from core import Constant, valuetypes, π, x
        from operations import Multiply

        """Applies mathematical rules to the expression
        and simplifies it to its simplest form."""

        if self.arg == π or self.arg == 0: # Sin(π) = Sin(0) = 0
                return Constant(0)
        
        elif isinstance(self.arg, Multiply):
            if self.arg.x == -1: # Sin(-x) = -Sin(x)
                return -Sin(self.arg.y)
            elif self.arg.y == -1: # Sin(-y) = Sin(y)
                return -Sin(self.arg.x)
            
            # Mechanism to reduce arg to range [0, 2π].
            if any(value==π for value in (self.arg.x, self.arg.y)):
                if self.arg.x == π and isinstance(self.arg.y, valuetypes):
                    self.arg.x, self.arg.y = self.arg.y, self.arg.x      
                self.arg.x = self.arg.x % 2
                self.arg.x = round(self.arg.x, 10)

                if self.arg.x in (0,1): # Sin(0π) = Sin(1π) = 0
                    return Constant(0)
                elif self.arg.x == 0.5: # Sin(0.5π) = 1
                    return Constant(1)
                elif self.arg.x == 1.5: # Sin(1.5π) = -1
                    return Constant(-1)
                
        if Sin.evaluate==True: # Evaluates Sin(arg) to a Constant value
            if isinstance(self.arg, valuetypes):
                return Sin(x).taylor(x, 20).express(self.arg.value, x)
            if isinstance(self.arg, Multiply):
                if self.arg.x == π and isinstance(self.arg.y, valuetypes):
                    return Sin(x).taylor(x, 20).express(π.value * self.arg.y, x)
                if self.arg.y == π and isinstance(self.arg.x, valuetypes):
                    return Sin(x).taylor(x, 20).express(π.value * self.arg.x, x)
        return self
    
    def __str__(self):
        """Represents Sin object as a string."""
        return f"sin({self.arg})"
    
    def diff(self, var):
        """Differentiates Sine object with respect to var.
        
        sin'(x) = x' * cos(x)"""
        return Cos(self.arg) * self.arg.diff(var)
    

class Cos(Unary):

    """Class representing mathematical Cosine function.
    Applies mathematical rules for simplifying expressions."""

    def simplified(self):

        from core import Constant, valuetypes, π, x
        from operations import Multiply

        """Applies mathematical rules to the expression
        and simplifies it to its simplest form."""

        if self.arg == π: # Cos(π) = -1
            return Constant(-1)
        elif self.arg == 0: # Cos(0) = 1
            return Constant(1)
        if isinstance(self.arg, Multiply):
            if self.arg.x == -1: # Cos(-x) = Cos(x)
                return Cos(self.arg.y)
            elif self.arg.y == -1: # Cos(-y) = Cos(y)
                return Cos(self.arg.x)
            
            # Mechanism to reduce arg to range [0, 2π].
            if any(value == π for value in (self.arg.x, self.arg.y)):
                if self.arg.x == π and isinstance(self.arg.y, valuetypes):
                    self.arg.x, self.arg.y = self.arg.y, self.arg.x                 
                self.arg.x = self.arg.x % 2
                self.arg.x = round(self.arg.x, 10)

                if self.arg.x in(0.5, 1.5): # Cos(0.5π) = Cos(1.5π) = 0
                    return Constant(0)
                if self.arg.x == 0: # Cos(0π) = 1
                    return Constant(1)
                if self.arg.x == 1: # Cos(1π) = -1
                    return Constant(-1)
                
        if Cos.evaluate == True: # Evaluates Cos(arg) to a Constant value
            if isinstance(self.arg, Constant):
                return Cos(x).taylor(x, 20).express(self.arg.value, x)
            if isinstance(self.arg, Multiply):
                if self.arg.y == π and isinstance(self.arg.x, valuetypes):
                    return Cos(x).taylor(x, 20).express(π.value * self.arg.x, x)
        return self
    
    def __str__(self):
        """Represents Cos object as a string."""
        return f"cos({self.arg})"
    
    def diff(self, var):
        """Differentiates Cos object with respect to var.
        
        cos'(x) = x' * -sin(x)"""
        return self.arg.diff(var) * -Sin(self.arg)


class Tan(Unary):

    """Class representing mathematical Tangent function.
    Applies mathematical rules for simplifying expressions."""

    def simplified(self):

        from core import Constant, valuetypes, π, x
        from operations import Multiply

        """Applies mathematical rules to the expression
        and simplifies it to its simplest form."""

        if self.arg == 0 or self.arg == π: # Tan(0) = Tan(π) = 0
            return Constant(0)
        if isinstance(self.arg, Multiply):
            if self.arg.x == -1: # Tan(-x) = -Tan(x)
                return -Tan(self.arg.y)
            elif self.arg.y == -1: # Tan(-y) = -Tan(y)
                return -Tan(self.arg.x)
            
            # Mechanism to reduce arg to range [0, 2π].
            if any(value == π for value in (self.arg.x, self.arg.y)):
                if self.arg.x == π and isinstance(self.arg.y, valuetypes):
                    self.arg.x, self.arg.y = self.arg.y, self.arg.x                 
                self.arg.x = self.arg.x % 1
                self.arg.x = round(self.arg.x, 10)

                if self.arg.x == 0: # Tan(0π) = 0
                    return Constant(0)
                if self.arg.x == 0.5: 
                    raise ZeroDivisionError("Tan(0.5π) is undefined")
                if self.arg.x == 0.25: # Tan(0.25π) = 1
                    return Constant(1)
                
        # Evaluates Tan(arg) to a Constant value by evaluating Sin(arg)/Cos(arg)
        if Tan.evaluate == True: 
            original = [Sin.evaluate, Cos.evaluate]
            Sin.evaluate, Cos.evaluate = True, True

            output = Sin(self.arg) / Cos(self.arg)
            Sin.evaluate, Cos.evaluate = original
            return output
        return self

    def __str__(self):
        """Represents Tan object as a string."""
        return f"tan({self.arg})"
    
    def diff(self,var):
        """Differentiates Tan object with respect to var.
        
        tan'(x) = x' * sec(x)**2"""
        return self.arg.diff(var) * Cos(self.arg) ** (-2)


class Ln(Unary):

    """Class representing natural logarithm.
    Applies mathematical rules for simplifying expressions."""

    def simplified(self):

        from core import Constant, Euler, x
        from operations import Multiply, Power

        e = Euler()
        
        """Applies mathematical rules to the expression
        and simplifies it to its simplest form."""

        if self.arg == 1: # ln(1) = 0
            return Constant(0)
        elif self.arg == e: # ln(e) = 1
            return Constant(1)
        if isinstance(self.arg, Multiply): # ln(xy) = ln(x) + ln(y)
            return Ln(self.arg.x) + Ln(self.arg.y)
        elif isinstance(self.arg, Power): # ln(x**y) = y*ln(x)
            return self.arg.y * Ln(self.arg.x)
        elif isinstance(self.arg, NaturalExp): # ln(e**x) = x
            return self.arg.arg
        
        # Approximates ln(arg) to a Constant value. Approximations valid for small values
        if Ln.evaluate == True:
            if isinstance(self.arg, Constant):
                return Ln(x).taylor(x, 20, 1).express(self.arg.value, x)
        return self
    
    def diff(self, var):
        """Differentiates Ln object with respect to var.
        
        ln'(x) = x'/x"""
        return self.arg.diff(var) / self.arg
    
    def __str__(self):
        """Represents Ln object as a string."""
        return f"ln({self.arg})"   


class NaturalExp(Unary):

    """Class representing natural exponential function.
    Applies mathematical rules for simplifying expressions."""

    def simplified(self):

        from core import Constant, e

        """Applies mathematical rules to the expression
        and simplifies it to its simplest form."""

        if self.arg == 0: # e ** 0 = 1
            return Constant(1)
        if self.arg == 1: # e ** 1 = e
            return e
        if isinstance(self.arg, Ln): # e ** ln(x) = x
            return self.arg.arg
        return self
    
    def diff(self, var):
        """Differentiates NaturalExp object with respect to var.
        
        (e ** x)' = e ** x * x'"""
        return self * self.arg.diff(var)

    def __str__(self):
        """Represents NaturalExp object as a string."""
        if isinstance(self.arg,Function):   
            return f"e ^ ({self.arg})"
        return f"e ^ {self.arg}"
