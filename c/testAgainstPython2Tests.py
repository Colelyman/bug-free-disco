import ctypes
from datetime import datetime
import glob
import os

import numpy as np


def parse_aln_matrix(path):
    with open(path) as path_fh:
        headers = None
        while headers is None:
            header_line = path_fh.readline().strip()
            if header_line[0] == '#':
                continue
            headers = [ord(x) for x in header_line.split(' ') if x]
        mat_size = max(headers) + 1

        a = np.zeros((mat_size, mat_size), dtype=np.int32)

        for ai, line in enumerate(path_fh):
            weights = [int(x) for x in line[:-1].split(' ')[1:] if x]
            for ohidx, weight in zip(headers, weights):
                a[headers[ai], ohidx] = weight

        return a


#get all generated test files
test_files = glob.glob("../generate.py.test*.test")

if os.path.exists('output.txt'):
    os.remove('output.txt')

alnMatrix = parse_aln_matrix('EDNAFULL')
fun = ctypes.CDLL('libfun.so')
fun.setup.argtypes = [np.ctypeslib.ndpointer(dtype=np.int32)]
fun.setup(alnMatrix)

fun.global_align.argtypes = [
    ctypes.c_char_p,
    ctypes.c_char_p,
    np.ctypeslib.ndpointer(dtype=np.int32),
]
fun.global_align.restype = ctypes.c_char_p

for test_file in test_files:
    print('Running tests in ' + test_file)
    py2_file = test_file+".python2_results.txt"
    test_count = 0
    s1 = datetime.now()
    #open the test file with sequences and the python results file
    with open(test_file,'r') as fin, open(py2_file,'r') as fpy2:
        #read the reference sequence from the test file
        ref_seq = fin.readline().strip().split("\t")[1].encode('utf-8')
        gap_incentive = np.zeros(len(ref_seq)+1,dtype=np.int32)

        #test all the cases in test (one sequence per line)
        line = fin.readline().strip()
        while line:
            test_count += 1
            #compute C result
            fun.global_align(
                line.encode('utf-8'),
                ref_seq,
                gap_incentive,
            )

            line = fin.readline().strip()
        # close the C output file
        fun.done()
        s2 = datetime.now()

        with open('output.txt', 'r') as fc:
            line = fc.readline().strip()
            while line:
                #get C results
                result_seq1, result_seq2, score = line.split('\t')
                #get python2 results
                result_seq1_py2,result_seq2_py2,score_py2 = fpy2.readline().split("\t")

                if result_seq1 != result_seq1_py2:
                    print('C result_seq1:%s\npython3 result_seq2:%s\npython3 score:%s\npython2 result_seq1:%s\npython2 result_seq2:%s\npython2 score:%s'%(result_seq1,result_seq2,str(score),result_seq1_py2,result_seq2_py2,score_py2))
                    raise Exception('Error - Alignment mismatch for %s\nGot       %s\nExpecting %s'%(line,result_seq1,result_seq1_py2))

                if result_seq2 != result_seq2_py2:
                    print('C result_seq1:%s\npython3 result_seq2:%s\npython3 score:%s\npython2 result_seq1:%s\npython2 result_seq2:%s\npython2 score:%s'%(result_seq1,result_seq2,str(score),result_seq1_py2,result_seq2_py2,score_py2))
                    raise Exception('Error - Alignment mismatch for %s\nGot       %s\nExpecting %s'%(line,result_seq2,result_seq2_py2))

                # round_score = str(round(float(score),8))
                # round_score_py2 = str(round(float(score_py2),8))
                # if round_score != round_score_py2:
                #     print('C result_seq1:%s\npython3 result_seq2:%s\npython3 score:%s\npython2 result_seq1:%s\npython2 result_seq2:%s\npython2 score:%s'%(result_seq1,result_seq2,str(score),result_seq1_py2,result_seq2_py2,score_py2))
                #     raise Exception('Error - Score mismatch for %s\nGot       %s\nExpecting %s'%(line,round_score,round_score_py2))
                line = fc.readline().strip()
    tdelta = s2-s1
    print('Performed ' + str(test_count) + ' tests in ' + str(tdelta) + ' seconds')

print('Testing passed')
