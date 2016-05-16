'''
Created on May 15, 2016

@author: Yuliya
'''
from poetifier.scorer import run_switcher

sentence1 = 'her eyes were red and puffy from many tears .'
sentence2 = 'One of the things I like most in life is food .'
sentence3 = 'A lifetime filled with cheating hearts ,'

if __name__ == '__main__':
    run_switcher(sentence3, 'parse3.trees')