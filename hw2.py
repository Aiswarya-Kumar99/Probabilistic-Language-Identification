import sys
import math
import re
from pathlib import Path
from collections import Counter

def get_parameter_vectors():
    '''
    This function parses e.txt and s.txt to get the  26-dimensional multinomial
    parameter vector (characters probabilities of English and Spanish) as
    descibed in section 1.2 of the writeup

    Returns: tuple of vectors e and s
    '''
    #Implementing vectors e,s as lists (arrays) of length 26
    #with p[0] being the probability of 'A' and so on
    e=[0]*26
    s=[0]*26

    with open('e.txt',encoding='utf-8') as f:
        for line in f:
            #strip: removes the newline character
            #split: split the string on space character
            char,prob=line.strip().split(" ")
            #ord('E') gives the ASCII (integer) value of character 'E'
            #we then subtract it from 'A' to give array index
            #This way 'A' gets index 0 and 'Z' gets index 25.
            e[ord(char)-ord('A')]=float(prob)
    f.close()

    with open('s.txt',encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            s[ord(char)-ord('A')]=float(prob)

    return (e,s)

def shred(filename):
    #Using a dictionary here. You may change this to any data structure of
    #your choice such as lists (X=[]) etc. for the assignment
    X={chr(i):0 for i in range(ord('A'),ord('Z')+1)}
    with open (filename,encoding='utf-8') as f:
        # TODO: add your code here
        content = f.read().upper()
        content = re.sub(r'[^A-Z]','',content)
        letterCount = Counter(content)
        X.update(letterCount)
    f.close()
    return X

def classify(e,s,count,engPrior,spanPrior):
    eng = math.log(engPrior)
    span = math.log(spanPrior)
    probAeng = count.get(chr(65)) * math.log(e[0])
    probAspan = count.get(chr(65)) * math.log(s[0])
    for i in range(0,26):
        e_prob = e[i] if e[i] > 0 else 1e-10
        s_prob = s[i] if s[i] > 0 else 1e-10
        eng += count.get(chr(i+65)) * math.log(e_prob)
        span += count.get(chr(i+65)) * math.log(s_prob)
    if span - eng >=100:
        probofEnglish = 0
    elif span - eng <= -100:
        probofEnglish = 1
    else:
        probofEnglish = 1 / (1 + (math.exp(span-eng)))
    return probAeng,probAspan,eng,span,probofEnglish


# TODO: add your code here for the assignment
# You are free to implement it as you wish!
# Happy Coding!
if len(sys.argv)<4:
    print("Please enter the file to read")
else:
    #1.1 Build your own digital shredder
    filepath = sys.argv[1]
    engPrior = sys.argv[2]
    spanPrior = sys.argv[3]
    count = shred(filepath)
    fileName = Path(filepath).stem
    outputFile = f"{fileName}_out"
    
    #1.2 Language identification via Bayes rule
    e,s = get_parameter_vectors()
    probAeng,probAspan,eng,span,probofEnglish = classify(e,s,count,float(engPrior),float(spanPrior))
    print("Q1")
    for char,freq in count.items():
            print(f"{char} {freq}")
    print("Q2")
    print(f"{probAeng:.4f}")
    print(f"{probAspan:.4f}")
    print("Q3")
    print(f"{eng:.4f}")
    print(f"{span:.4f}")
    print("Q4")
    print(f"{probofEnglish:.4f}")  