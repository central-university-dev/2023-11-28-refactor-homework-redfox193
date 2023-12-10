from typing import Union
import some.module.A


class B(A): # rename class when inherit from it
    pass

a = A() # rename class when create an instance

def foo(p: A): # annotation renaming
    return A # rename when return

def foo3(p: A | int): # annotation renaming
    pass

def foo2(p: Union[A, A]): # annotation renaming
    pass

foo(A) # rename when pass as an argument