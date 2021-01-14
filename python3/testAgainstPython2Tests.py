import numpy as np
import CRISPResso2Align as nw
import glob
from datetime import datetime
alnMatrix = nw.read_matrix("EDNAFULL")

#get all generated test files
test_files = glob.glob("../generate.py.test*.test")

for test_file in test_files:
    print('Running tests in ' + test_file)
    py2_file = test_file+".python2_results.txt"
    test_count = 0
    s1 = datetime.now()
    #open the test file with sequences and the python results file
    with open(test_file,'r') as fin, open(py2_file,'r') as fpy2:
        #read the reference sequence from the test file
        ref_seq = fin.readline().strip().split("\t")[1].encode('utf-8')
        gap_incentive = np.zeros(len(ref_seq)+1,dtype=np.int)

        #test all the cases in test (one sequence per line)
        line = fin.readline().strip()
        while line:
            test_count += 1
            #compute python3 result
            result_seq1,result_seq2,score = nw.global_align(line.encode('utf-8'),ref_seq, matrix=alnMatrix,gap_incentive =gap_incentive)
            #get python2 results
            result_seq1_py2,result_seq2_py2,score_py2 = fpy2.readline().split("\t")

            if result_seq1.decode() != result_seq1_py2:
                print('python3 result_seq1:%s\npython3 result_seq2:%s\npython3 score:%s\npython2 result_seq1:%s\npython2 result_seq2:%s\npython2 score:%s'%(result_seq1.decode(),result_seq2.decode(),str(score),result_seq1_py2,result_seq2_py2,score_py2))
                raise Exception('Error - Alignment mismatch for %s\nGot       %s\nExpecting %s'%(line,result_seq1.decode(),result_seq1_py2))
        
            if result_seq2.decode() != result_seq2_py2:
                print('python3 result_seq1:%s\npython3 result_seq2:%s\npython3 score:%s\npython2 result_seq1:%s\npython2 result_seq2:%s\npython2 score:%s'%(result_seq1.decode(),result_seq2.decode(),str(score),result_seq1_py2,result_seq2_py2,score_py2))
                raise Exception('Error - Alignment mismatch for %s\nGot       %s\nExpecting %s'%(line,result_seq2.decode(),result_seq2_py2))

            round_score = str(round(float(score),8))
            round_score_py2 = str(round(float(score_py2),8))
            if round_score != round_score_py2:
                print('python3 result_seq1:%s\npython3 result_seq2:%s\npython3 score:%s\npython2 result_seq1:%s\npython2 result_seq2:%s\npython2 score:%s'%(result_seq1.decode(),result_seq2.decode(),str(score),result_seq1_py2,result_seq2_py2,score_py2))
                raise Exception('Error - Score mismatch for %s\nGot       %s\nExpecting %s'%(line,round_score,round_score_py2))
            line = fin.readline().strip()
    s2 = datetime.now()
    tdelta = s2-s1
    print('Performed ' + str(test_count) + ' tests in ' + str(tdelta) + ' seconds')

print('Testing passed')
