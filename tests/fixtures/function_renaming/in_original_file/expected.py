from typing import Any


def myfunc(arg1: int, arg2: str) -> str: # function definition
    return "Hello"


def other_foo(p: Any) -> Any:
    return myfunc # return function

other_foo(myfunc) 

myfunc(2, "str") # call function

a = myfunc # assign function
b, c = myfunc, 1 # multiple assignement

l = ["element 1", myfunc, 2, (myfunc, 2)] # function as an element