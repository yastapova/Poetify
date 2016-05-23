'''
Created on May 15, 2016

@author: Yuliya
'''
from poetifier.scorer import run_switcher, swapper

sentence1 = 'her eyes were red and puffy from many tears.'
sentence2 = 'One of the things I like most in life is food.'
sentence3 = 'A lifetime filled with cheating hearts,'
sentence4 = 'Cat videos are a pretty good way to pass the time!'
sentence5 = 'So I smouched one, and they come out nine same as the other time.'
sentence6 = 'She completed the race first because she ran quickly.'
sentence7 = 'We had not started a moment too soon.'

if __name__ == '__main__':
    run_switcher('parse7.trees')
    #run_switcher('../data/class_test.trees')