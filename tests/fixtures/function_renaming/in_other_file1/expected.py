from typing import Any
import module
import some.module.myfunc


def other_foo(p: Any) -> Any:
    return myfunc # return imported function

other_foo(myfunc) 

myfunc(2, "str") # call imported function

a = myfunc # assign imported function
b, c = myfunc, 1 # multiple assignement

l = ["element 1", myfunc, 2, (myfunc, 2)] # imported function as an element