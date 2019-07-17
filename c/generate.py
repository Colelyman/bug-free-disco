import random

pool = ['A', 'T', 'C', 'G']

def stringconstruct():
    string = []
    for i in range(random.randint(1, 200)):
        string.append(pool[random.randint(0, 3)])
    string = ''.join(string)
    return string


def stringmutate(string):
    string = list(string)
    for i in range(random.randint(0, 20)):
        mutationtype = random.randint(0, 2)
        # 0 - swap, 1 - insertion, 2 - deletion
        
        if (mutationtype == 0):
            string[random.randint(0, len(string)-1)] = pool[random.randint(0, 3)]
        
        if (mutationtype == 1):
            string.insert(random.randint(0,len(string)-1), pool[random.randint(0, 3)])
        
        if (mutationtype == 2):
            string.insert(random.randint(0,len(string)-1), pool[random.randint(0, 3)])
    
    string = ''.join(string)
    return(string)

testno = 0
outF = open("randtests.txt", "w")
while testno < 50000:
    a = stringconstruct()
    b = stringmutate(a)
    line = a + '\t' + b
    outF.write(line)
    outF.write("\n")
    testno += 1
    print(testno)
outF.close()





