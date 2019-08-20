import ctypes 
import numpy
import os
# libfun loaded to the python file 
# using fun.myFunction(), 
# C function can be accessed 
# but type of argument is the problem. 




#################################################################
ai = 0
fh = open("EDNAFULL")
headers = None
while headers is None:
    line = fh.readline().strip()
    if line[0] == '#': continue
    headers = [ord(x) for x in line.split(' ') if x]
mat_size = max(headers) + 1

a = numpy.zeros((mat_size, mat_size), dtype=numpy.int32)

line = fh.readline()
while line:
    line_vals = [int(x) for x in line[:-1].split(' ')[1:] if x]
    for ohidx, val in zip(headers, line_vals):
        a[headers[ai], ohidx] = val
    ai += 1
    line = fh.readline()
#################################################################

                         
fun = ctypes.CDLL(os.path.join(os.getcwd(),'libfun.so')) 



fun.setup.argtypes = [numpy.ctypeslib.ndpointer(dtype=numpy.int32)]


fun.setup(a)

fun.global_align.argtypes = [ctypes.c_char_p,ctypes.c_char_p,numpy.ctypeslib.ndpointer(dtype=numpy.int32)]
fun.global_align.restype = ctypes.c_char_p # specify return type. Default is int


with open('../randtests.txt', 'r') as test_file:
	line = test_file.readline()
	while line:

		line_els = line.split('\t')
		seq1 = line_els[0]
		seq2 = line_els[1]

		gap_incentive = numpy.zeros(len(seq2)+1, numpy.int32)
		fun.global_align(seq1, seq2, gap_incentive)

		line = test_file.readline()





# Now whenever argument  
# will be passed to the function                                                         
# ctypes will check it.

fun.done() #make sure to close output file.


# argtype for 1d int array: numpy.ctypeslib.ndpointer(dtype=numpy.int32)