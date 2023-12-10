from typing import Union
import module1, module2
from module3 import A1, A2
from some import module

class A:
    pass

class B(A): # rename class when inherit from it
    pass

a = module.A() # rename class when create an instance
a = A()

def foo(p: module.A): # annotation renaming
    return module.A # rename when return

def foo3(p: module.A | A | A2): # annotation renaming
    pass

def foo2(p: Union[module.A, A1]): # annotation renaming
    pass

foo(module.A) # rename when pass as an argument