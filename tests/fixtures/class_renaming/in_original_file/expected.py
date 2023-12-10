from typing import Union

class C: # rename class def
    def foo(self):
        pass

class B(C): # rename class when inherit from it
    pass

a = C() # rename class when create an instance

a.foo()

def foo(p: C): # annotation renaming
    return C # rename when return

def foo3(p: C | C | C): # annotation renaming
    pass

def foo2(p: Union[C, int]): # annotation renaming
    pass

foo(C) # rename when pass as an argument