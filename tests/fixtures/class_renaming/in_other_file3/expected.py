from typing import Union
import module1, module2
from module3 import A1, A2
from some import module

class A:
    pass

class B(A): # rename class when inherit from it
    pass

a = module.C() # rename class when create an instance
a = A()

def foo(p: module.C): # annotation renaming
    return module.C # rename when return

def foo3(p: module.C | A | A2): # annotation renaming
    pass

def foo2(p: Union[module.C, A1]): # annotation renaming
    pass

foo(module.C) # rename when pass as an argument