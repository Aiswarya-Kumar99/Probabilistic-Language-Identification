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
    f.close()

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
    return X



# TODO: add your code here for the assignment
# You are free to implement it as you wish!
# Happy Coding!
if len(sys.argv)<2:
    print("Please enter the file to read")
else:
    filepath = sys.argv[1]
    count = shred(filepath)
    fileName = Path(filepath).stem
    outputFile = f"{fileName}_out"
    with open(outputFile,'w') as f:
        f.write("Q1\n")
        for char,freq in count.items():
            f.write(f"{char} {freq}\n")