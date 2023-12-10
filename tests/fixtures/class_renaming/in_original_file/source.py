from typing import Union

class A: # rename class def
    def foo(self):
        pass

class B(A): # rename class when inherit from it
    pass

a = A() # rename class when create an instance

a.foo()

def foo(p: A): # annotation renaming
    return A # rename when return

def foo3(p: A | A | A): # annotation renaming
    pass

def foo2(p: Union[A, int]): # annotation renaming
    pass

foo(A) # rename when pass as an argument