from typing import Any
import module
import some.module.foo


def other_foo(p: Any) -> Any:
    return foo # return imported function

other_foo(foo) 

foo(2, "str") # call imported function

a = foo # assign imported function
b, c = foo, 1 # multiple assignement

l = ["element 1", foo, 2, (foo, 2)] # imported function as an element