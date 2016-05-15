'''
Created on May 14, 2016

@author: Yuliya
'''
import sys
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

pcfg_file_path = '../pcfg/pcfg.txt'
all_rules = False
sentence = 'her eyes were red and puffy from many tears .'

def run_switcher(s):
    print('Reading pcfg file.', flush=True)
    u_lhs, tags, rules, probs, ntags, nwords = parsepcfg.parse_grammar(pcfg_file_path)
    print('Creating parse tree for input.', flush=True)
    parsepcfg.create_trees(all_rules, sentence, u_lhs, tags, rules, probs, ntags, nwords)
    print('Created parse.trees file.', flush=True)
    parse = runner.read_file('parse.trees')
    parse = parse.strip().split('\n')
    print('Getting rules used in parse.', flush=True)
    ptree = [tree.Tree.from_str(parse[0])]
    rules_p, u_lhs_p, u_tags_p, words_p = trainpcfg.count_all_rules(ptree)
    
run_switcher(sentence)