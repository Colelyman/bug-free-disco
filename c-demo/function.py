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
retVal = fun.myFunction(16,'TEST')      

print('return value is ' + str(retVal))
