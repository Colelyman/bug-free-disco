import numpy as np
import CRISPResso2Align as nw
import glob
from datetime import datetime
alnMatrix = nw.read_matrix("EDNAFULL")


test_files = glob.glob("../generate.py.test*.test")

for test_file in test_files:
    print('Running tests in ' + test_file)
    p2_file = test_file+".python2_results.txt"
    test_count = 0
    s1 = datetime.now()
    with open(test_file,'r') as fin, open(p2_file,'w') as fout:
        ref_seq = fin.readline().strip().split("\t")[1]
        gap_incentive = np.zeros(len(ref_seq)+1,dtype=np.int)
        line = fin.readline().strip()
        while line:
            test_count += 1
            result_seq1,result_seq2,score=nw.global_align(line,ref_seq, matrix=alnMatrix,gap_incentive =gap_incentive)
            fout.write("\t".join([result_seq1,result_seq2,str(score)])+"\n")
            line = fin.readline().strip()
    s2 = datetime.now()
    tdelta = s2-s1
    print('Performed ' + str(test_count) + ' tests in ' + str(tdelta) + ' seconds')
