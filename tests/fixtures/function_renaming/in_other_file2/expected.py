from typing import Any
import module1, module2
from module3 import func1, func2
from some.module import myfunc, foo1


def other_foo(p: Any) -> Any:
    return myfunc # return imported function

other_foo(myfunc) 

myfunc(2, "str") # call imported function

a = myfunc # assign imported function
b, c = myfunc, 1 # multiple assignement

l = ["element 1", myfunc, 2, (myfunc, 2)] # imported function as an element