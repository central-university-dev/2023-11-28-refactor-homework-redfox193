from typing import Any
import module1, module2
from module3 import func1, func2
from some.module import foo, foo1


def other_foo(p: Any) -> Any:
    return foo # return imported function

other_foo(foo) 

foo(2, "str") # call imported function

a = foo # assign imported function
b, c = foo, 1 # multiple assignement

l = ["element 1", foo, 2, (foo, 2)] # imported function as an element