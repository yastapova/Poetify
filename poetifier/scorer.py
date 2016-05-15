'''
Created on May 14, 2016

@author: Yuliya
'''
import sys
from math import log,exp
sys.path.append('..')
from pcfg import parsepcfg, trainpcfg, runner, tree

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

def run_switcher(s):
    print('Reading pcfg file.', flush=True)
    u_lhs, tags, rules, probs, ntags, nwords = parsepcfg.parse_grammar(pcfg_file_path)
    print('Creating parse tree for input.', flush=True)
    #parsepcfg.create_trees(all_rules, s, u_lhs, tags, rules, probs, ntags, nwords)
    print('Created parse.trees file.', flush=True)
    parse = runner.read_file('parse.trees')
    parse = parse.strip().split('\n')
    print('Getting rules used in parse.', flush=True)
    ptree = [tree.Tree.from_str(parse[0])]
    rules_p, u_lhs_p, u_tags_p, words_p = trainpcfg.count_all_rules(ptree)
    ascore, mscore = calc_score(rules, probs, rules_p, u_lhs, ntags, nwords)
    print('scores:\t' + str(ascore/len(rules_p)) + '\t' + str(mscore/len(rules_p)))
    from poetifier import sentence_classifier
    sentence_classifier.classify_input(s, [ascore, mscore])
    
#run_switcher(sentence3)