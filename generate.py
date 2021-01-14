import random
import os

pool = ['A', 'T', 'C', 'G']
num_tests = 10000 #number of test cases
str_min_len = 100 #min and max lens of strings to produce
str_max_len = 300
num_mods = 3 #max number of modifications (indels) to introduce

def stringconstruct():
    string = []
    for i in range(random.randint(str_min_len, str_max_len)):
        string.append(pool[random.randint(0, 3)])
    string = ''.join(string)
    return string


def stringmutate(string):
    a = list(string)
#    print('str is ' + str(len(string)))
    aln_a = a[:]
    aln_b = a[:]
    b = a[:]
    this_num_mutations = random.randint(0,num_mods)
#    print('doing ' + str(this_num_mutations) +'mods')
    for i in range(this_num_mutations):
        mutationtype = random.randint(0, 2)
        # 0 - swap, 1 - insertion, 2 - deletion
        
        if (mutationtype == 0):
            aln_a[random.randint(0, len(a)-1)] = pool[random.randint(0, 3)]
        
        if (mutationtype == 1):
            ins_len = random.randint(1,3)
            ins_start = random.randint(0,len(a)-(ins_len+1))
            ins_end = ins_start + ins_len
#            print('ins from ' + str(ins_start) + ' to ' + str(ins_end))
            for i in range(ins_start,ins_end):
                aln_a[i] = "-"
        
        if (mutationtype == 2):
            del_len = random.randint(1,3)
            del_start = random.randint(0,len(a)-(del_len+1))
            del_end = del_start + del_len
#            print('del from ' + str(del_start) + ' to ' + str(del_end))
            for i in range(del_start,del_end):
                aln_b[i] = "-"
    
    str_aln_a = ''.join(aln_a)
    str_aln_b = ''.join(aln_b)
    str_a = str_aln_a.replace("-","")
    str_b = str_aln_b.replace("-","")
    return(str_a,str_b,str_aln_a,str_aln_b)

file_index = 0
file_name = "generate.py.test"+str(file_index)+".test"
while os.path.exists(file_name):
    file_index += 1
    file_name = "generate.py.test"+str(file_index)+".test"

outF = open(file_name, "w")
this_string = stringconstruct()
outF.write("WT\t" + this_string+"\n")
testno = 0
while testno < num_tests:
    a,b,aln_a, aln_b = stringmutate(this_string)
    outF.write(b+"\n")
    testno += 1
outF.close()
print('wrote ' + str(testno) + ' to ' + file_name)





