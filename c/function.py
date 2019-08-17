import ctypes 
import numpy
import os
# libfun loaded to the python file 
# using fun.myFunction(), 
# C function can be accessed 
# but type of argument is the problem. 
                         
fun = ctypes.CDLL(os.path.join(os.getcwd(),'libfun.so')) 

fun.setup()


seqj = "ACTGCT"
seqi = "ACTCTAA"
gap_incentive = numpy.zeros(len(seqi), numpy.int32)


# Now whenever argument  
# will be passed to the function                                                         
# ctypes will check it.
fun.global_align.argtypes = [ctypes.c_char_p,ctypes.c_char_p,numpy.ctypeslib.ndpointer(dtype=numpy.int32)]
fun.global_align.restype = ctypes.c_char_p # specify return type. Default is int
fun.global_align(seqj, seqi, gap_incentive)


# argtype for 1d int array: numpy.ctypeslib.ndpointer(dtype=numpy.int32)