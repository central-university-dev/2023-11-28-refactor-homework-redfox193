from typing import Union
import module1, module2
from module3 import A1, A2
from some.module import C, foo1


class B(C): # rename class when inherit from it
    pass

a = C() # rename class when create an instance
a = A1()

def foo(p: C): # annotation renaming
    return C # rename when return

def foo3(p: C | int | A2): # annotation renaming
    pass

def foo2(p: Union[C, A1]): # annotation renaming
    pass

foo(C) # rename when pass as an argument