import numpy as np
import CRISPResso2Align as nw
alnMatrix = nw.read_matrix("EDNAFULL")

#py3results = open("py3results.db", "w")
with open('../randtests.txt','rb') as test_file:
    #head = test_file.readline()
    line = test_file.readline()
    while line:
        #print ("line: " + line)
        line_els = line.split(b'\t')
        seq1 = line_els[0]
        seq2 = line_els[1]
        #exp_result_seq1 = line_els[2]
        #exp_result_seq2 = line_els[3]
        #exp_score = line_els[4]

        gap_incentive = np.zeros(len(seq2)+1,dtype=np.int)
        result_seq1,result_seq2,score=nw.global_align(seq1, seq2, matrix=alnMatrix,gap_incentive =gap_incentive)


        #print(result_seq1)
        #print(result_seq2)

        #resultline = str(result_seq1, 'utf-8') + '\t' + str(result_seq2, 'utf-8')
        #py3results.write(resultline)
        # print('score: ' + str(score))
        # if str(result_seq1, 'utf-8') != exp_result_seq1:
        #     raise Exception("ERROR. Got " + str(result_seq1, 'utf-8') + " but expecting " + exp_result_seq1)
        # if str(result_seq2, 'utf-8') != exp_result_seq2:
        #     raise Exception("ERROR. Got " + str(result_seq2, 'utf-8') + " but expecting " + exp_result_seq2)
        line = test_file.readline()

