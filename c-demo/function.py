import ctypes 
import os
# libfun loaded to the python file 
# using fun.myFunction(), 
# C function can be accessed 
# but type of argument is the problem. 
                         
fun = ctypes.CDLL(os.path.join(os.getcwd(),'libfun.so'))
# Now whenever argument  
# will be passed to the function                                                         
# ctypes will check it. 
            
fun.myFunction.argtypes = [ctypes.c_int,ctypes.c_char_p]

  
# now we can call this  
# function using instant (fun) 
# returnValue is the value  
# return by function written in C  
# code      

fun.myFunction.restype = ctypes.c_char_p
# this is needed to specify
# the return type for strings.
# Otherwise default is int and 
# it will return a memory address.


retVal = fun.myFunction(1, "TEST")

print('return value is ' + str(retVal))
