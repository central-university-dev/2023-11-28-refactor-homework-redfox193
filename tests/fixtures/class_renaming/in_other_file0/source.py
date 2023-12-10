from typing import Union
import some.module

class A: # do not rename this class
    pass

a = A()

class B(module.A): # rename class when inherit from it
    pass

a = module.A() # rename class when create an instance

def foo(p: module.A): # annotation renaming
    return module.A # rename when return

def foo3(p: module.A | A): # annotation renaming
    pass

def foo2(p: Union[module.A, A]): # annotation renaming
    pass

foo(module.A) # rename when pass as an argument