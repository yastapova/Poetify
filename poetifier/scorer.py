'''
Created on May 14, 2016

@author: Yuliya
'''
import sys
from math import log,exp
sys.path.append('..')
from pcfg import parsepcfg, trainpcfg, runner, tree
import numpy as np

# input a single sentence

# run pcfg on sentence to get parse Tree
    # read pcfg file and construct grammar
    # run sentence through grammar
    # extract rules from parse tree
    # return parse tree string, rules used

# determine poetic score
    # read rules used
    # take their probabilities from pcfg
    # sum of probabilities = score?
    # product of probabilities = score?
    
# swap phrases at random points
    # make sure to cover all points
    # determine the poetic scores of each switch
    # keep track of max score and switch
    
# max score is the winner

def calc_score(rules, probs, p_rules, u_lhs, ntags, nwords):
    ascore = 0
    mscore = 0
    for r in p_rules:
        temp = parsepcfg.get_Laplace_prob(r, probs, u_lhs, ntags, nwords)
        #print('rule: ' + str(r) + '\tscore: ' + str(temp))
        ascore = ascore + temp
        mscore = mscore + log(temp)
    return ascore, exp(mscore)

pcfg_file_path = '../pcfg/pcfg.txt'
all_rules = False


def switcher(r):
    if r == None:
        return
    if len(r.children) != 2:
        return
    t = r.children[0]
    r.children[0] = r.children[1]
    r.children[1] = t
    
def mega_swap(t):
    perms = []
    r = t.root
    if(len(r.children) == 1):
        r = r.children[0]
    if(r.children[1].label == '.'):
        r = r.children[0]
    for i in range(0, 2):
        si = format(i, '01b')
        try:
            if si[0] == '1':
                switcher(r)
        except IndexError:
            None
        
        for j in range(0, 4):
            sj = format(j, '02b')
            try:
                if sj[0] == '1':
                    switcher(r.children[0])
                if sj[1] == '1':
                    switcher(r.children[1])
            except IndexError:
                None
            #print(t.__str2__())
            
            for k in range(0, 16):
                sk = format(k, '04b')
                try:
                    if sk[0] == '1':
                        switcher(r.children[0].children[0])
                    if sk[1] == '1':
                        switcher(r.children[0].children[1])
                    if sk[2] == '1':
                        switcher(r.children[1].children[0])
                    if sk[3] == '1':
                        switcher(r.children[1].children[1])
                except IndexError:
                    None
                #print(t.__str2__())
                
                for l in range(0, 256):
                    progress = i*16384 + j*4096 + k*256 + l
                    total = 2*4*16*256
                    if((progress/total*100)%10 == 0):
                        print('[Progress] ' + str(progress/total*100) + '%')
                    sl = format(l, '08b')
                    try:
                        if sl[0] == '1':
                            switcher(r.children[0].children[0].children[0])
                        if sl[1] == '1':
                            switcher(r.children[0].children[0].children[1])
                        if sl[2] == '1':
                            switcher(r.children[0].children[1].children[0])
                        if sl[3] == '1':
                            switcher(r.children[0].children[1].children[1])
                        if sl[4] == '1':
                            switcher(r.children[1].children[0].children[0])
                        if sl[5] == '1':
                            switcher(r.children[1].children[0].children[1])
                        if sl[6] == '1':
                            switcher(r.children[1].children[1].children[0])
                        if sl[7] == '1':
                            switcher(r.children[1].children[1].children[1])
                    except IndexError:
                        None
                    
                    #print(t.__str2__())
                    if(t.__str__() not in perms):
                        perms.append(t.__str__())
                    
                    try:
                        if sl[0] == '1':
                            switcher(r.children[0].children[0].children[0])
                        if sl[1] == '1':
                            switcher(r.children[0].children[0].children[1])
                        if sl[2] == '1':
                            switcher(r.children[0].children[1].children[0])
                        if sl[3] == '1':
                            switcher(r.children[0].children[1].children[1])
                        if sl[4] == '1':
                            switcher(r.children[1].children[0].children[0])
                        if sl[5] == '1':
                            switcher(r.children[1].children[0].children[1])
                        if sl[6] == '1':
                            switcher(r.children[1].children[1].children[0])
                        if sl[7] == '1':
                            switcher(r.children[1].children[1].children[1])
                    except IndexError:
                        None
                
                try:
                    if sk[0] == '1':
                        switcher(r.children[0].children[0])
                    if sk[1] == '1':
                        switcher(r.children[0].children[1])
                    if sk[2] == '1':
                        switcher(r.children[1].children[0])
                    if sk[3] == '1':
                        switcher(r.children[1].children[1])
                except IndexError:
                    None
            
            try:
                if sj[0] == '1':
                    switcher(r.children[0])
                if sj[1] == '1':
                    switcher(r.children[1])
            except IndexError:
                None
        
        try:
            if si[0] == '1':
                switcher(r)
        except IndexError:
            None
    return perms

def swapper(testtrees):
    print('Beginning permutation swapping.',flush=True)
    perms = mega_swap(testtrees)
    #print(perms)
    return perms

def perm_scores(perms, rules, probs, u_lhs, ntags, nwords):
    print('Calculating permutation scores.',flush=True)
    scores = []
    for p in perms:
        rules_p, _, _, _ = trainpcfg.count_all_rules([tree.Tree.from_str(p)])
        #print(p)
        ascore, mscore = calc_score(rules, probs, rules_p, u_lhs, ntags, nwords)
        scores.append([ascore, mscore])
    return scores

def run_switcher(file):
    testing_mode = False
    print('Reading pcfg file.', flush=True)
    u_lhs, tags, rules, probs, ntags, nwords = parsepcfg.parse_grammar(pcfg_file_path)
    
    #print('Creating parse tree for input.', flush=True)
    #parsepcfg.create_trees(all_rules, s, u_lhs, tags, rules, probs, ntags, nwords)
    #print('Created ' + file + ' file.', flush=True)
    
    parse = runner.read_file(file)
    parse = parse.strip().split('\n')
    #print(len(parse))
    
    if(len(parse) > 1):
        testing_mode = True
        ptrees = [tree.Tree.from_str(x) for x in parse]
        #print(ptrees)
        scores = []
        for p in ptrees:
            rules_p, _, _, _ = trainpcfg.count_all_rules([p])
            a, m = calc_score(rules, probs, rules_p, u_lhs, ntags, nwords)
            scores.append([a, m])
            rules_p = []
        #print(scores)
        perms = ptrees

    print('Getting rules used in parse.', flush=True)
    if(not testing_mode):
        ptree = tree.Tree.from_str(parse[0])
        perms = swapper(ptree)
        scores = perm_scores(perms, rules, probs, u_lhs, ntags, nwords)
        #print(scores)
    
    from poetifier import sentence_classifier
    sentence_classifier.classify_input(perms, scores, testing_mode)
    
#run_switcher(sentence3)