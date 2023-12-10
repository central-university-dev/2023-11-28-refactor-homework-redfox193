from typing import Any


def foo(arg1: int, arg2: str) -> str: # function definition
    return "Hello"


def other_foo(p: Any) -> Any:
    return foo # return function

other_foo(foo) 

foo(2, "str") # call function

a = foo # assign function
b, c = foo, 1 # multiple assignement

l = ["element 1", foo, 2, (foo, 2)] # function as an element