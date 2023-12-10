from typing import Union
import some.module

class A: # do not rename this class
    pass

a = A()

class B(module.C): # rename class when inherit from it
    pass

a = module.C() # rename class when create an instance

def foo(p: module.C): # annotation renaming
    return module.C # rename when return

def foo3(p: module.C | A): # annotation renaming
    pass

def foo2(p: Union[module.C, A]): # annotation renaming
    pass

foo(module.C) # rename when pass as an argument