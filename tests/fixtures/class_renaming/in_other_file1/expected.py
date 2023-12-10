from typing import Union
import some.module.C


class B(C): # rename class when inherit from it
    pass

a = C() # rename class when create an instance

def foo(p: C): # annotation renaming
    return C # rename when return

def foo3(p: C | int): # annotation renaming
    pass

def foo2(p: Union[C, C]): # annotation renaming
    pass

foo(C) # rename when pass as an argument