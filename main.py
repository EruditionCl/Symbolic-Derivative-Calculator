
from core import *
from operations import * 
from functions import *

x=Variable("x") 
y=Variable("y")
z=Variable("z")
e=Euler()
pi=Pi()

a = x**Sin(x)
print(a.orderdiff(x,3))