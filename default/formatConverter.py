'''
Created on Apr 27, 2016
Takes in text representations of parse trees done
by the Stanford Parser, and converts them to a format
usable with my older code.

@author: Yuliya
'''

import argparse, sys
sys.path.append('..')

parser = argparse.ArgumentParser(description='Converts format of parse tree from Stanford Parser.')
parser.add_argument('-c', nargs=2, metavar=('input_file', 'output_file'), type=str,
                    help='Converts the given file to format usable by my application.')

args = parser.parse_args()
c = args.c

# opens a file and reads it
def read_file(name):
    print('Reading ' + name, flush=True)
    f = open(name, 'r')
    input_file = f.read()
    f.close()
    return(input_file)

# moves paren from before tag to after
def move_paren(s):
    if(len(s) == 1):
        return s
    # open paren means it should be moved
    elif(s[0:1] == '('):
        i = 0
        # go through and find its new position
        # which is determined by a space ' '
        while(s[i:i+1] != ' '):
            i += 1
        return s[1:i] + s[0:1] + move_paren(s[i+1:len(s)])
    # not open paren, leave it and keep going
    else:
        return s[0:1] + move_paren(s[1:len(s)])
    
# find where to put the underscore and place it
def underscore(s):
    i = 0
    j = i
    
    # move j to the first '('
    while(s[j:j+1] != '('):
        j += 1
    t1 = s[i:j] # first tag name has been found
    
    i = j + 1   # jump forward into the 2nd tag
    j = i
    # move j to the first '('
    while(s[j:j+1] != '('):
        j += 1
    t2 = s[i:j] # second tag name found
    
    # combine
    return t1 + '_' + t2 + s[j:len(s)-1]

# isolate the first fully closed group
# replace fully closed groups that only have one child
# by combining the tag names with an underscore '_'
def check_group(s):
    i = 0
    p = 0   # count of open parens
    hitOne = 0  # how many times there is only one open paren
    
    while(s[i:i+1] != '('):
        i += 1  # start at i = first paren
    for i in range(i, len(s)):
        c = s[i:i+1]
        if(c == '('):
            p += 1
            if(p == 1):
                hitOne += 1
        elif(c == ')'):
            p -= 1
            if(p == 1):
                hitOne += 1
        # if p == 0, there is a fully closed group
        # break to check how many child groups it contains
        if(p == 0):
            break
    # if hitOne == 2, it has only one child group
    # so combine with an underscore
    if(hitOne == 2):
        return underscore(s[0:i]) + ')' + s[i+1:len(s)]
    # otherwise, needs no modification
    return s

# modifies sentences to deal with groups that need underscores
def clean_tree(s):
    i = 0
    j = i
    temp = s
    
    # loop through entire sentence
    while(i < len(temp)):
        c = temp[i:i+1]
        # if the current character is a '('
        if(c == '('):
            j = i - 1
            # walk back to the start of the tag
            while(j > 0 and temp[j:j+1] != '(' and temp[j:j+1] != ')'):
                j -= 1
            # check if next group needs underscores
            temp = temp[0:j] + check_group(temp[j:len(temp)])
        i += 1
    
    return temp

# runs the format conversion on one sentence
def parse_sentence(s):
    return clean_tree(move_paren(s))

# fixes all of the sentences in a given input file
# and writes the resulting fixed sentences in the given output file
def parse(c_in, c_out):
    c_in = read_file(c_in)
    c_in = c_in.strip().split('\n')
    c_out = open(c_out, 'w')
    count = 1
    for s in c_in:
        print('Parsing:\t' + str(count) + ' of ' + str(len(c_in)))
        s = s[6:len(s)-1]   # get rid of ROOT tag
        # add TOP tag to comply with previous code
        res = 'TOP(' + parse_sentence(s) + ')'
        #print(res)
        c_out.write(res + '\n')
        #print()
        count += 1
    c_out.close()
  
'''
# sample parameters for testing
c = []
c.append('ex.txt')
c.append('exresult.txt')
'''
sys.setrecursionlimit(1500)
    
if(c != None):
    parse(c[0], c[1])