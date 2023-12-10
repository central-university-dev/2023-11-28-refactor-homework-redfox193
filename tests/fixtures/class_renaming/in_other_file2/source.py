from typing import Union
import module1, module2
from module3 import A1, A2
from some.module import A, foo1


class B(A): # rename class when inherit from it
    pass

a = A() # rename class when create an instance
a = A1()

def foo(p: A): # annotation renaming
    return A # rename when return

def foo3(p: A | int | A2): # annotation renaming
    pass

def foo2(p: Union[A, A1]): # annotation renaming
    pass

foo(A) # rename when pass as an argument