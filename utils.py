

def setconstant(*args):
    from core import Constant

    """Accepts any numerical value and converts it to class Constant.

    Args:
        args: An arbitrary number of values (ints, floats or Constant)

    Returns:
        result: A tuple of class Constant of these values.  
    """

    result = []
    for arg in args:
        if isinstance(arg, (int, float)):
            result.append(Constant(arg))
        else:
            result.append(arg)
    return tuple(result)

def factorial(input):

    """Accepts any int value and applies the mathematical factorial operation (x!)"""

    if not isinstance(input, int):
        raise TypeError("input in factorial() must be a int")
    elif input < 0:
        raise ValueError("input in factorial() must be greater than zero")
    elif input == 0:
        return 1
    else:
        output = 1
        for i in range(input):
            output *= (i + 1)
        return output
    