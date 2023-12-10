from typing import Any
import module1, module2
from module3 import func1, func2
from some import module


def foo(arg1: int, arg2: str): # do not touch this func
    return (arg1, arg2)

def other_foo(p: Any) -> Any:
    return module.myfunc # return imported function

other_foo(module.myfunc) 

module.myfunc(2, "str") # call imported function

a = module.myfunc # assign imported function
b, c = module.myfunc, 1 # multiple assignement

l = ["element 1", module.myfunc, 2, (module.myfunc, 2)] # imported function as an element