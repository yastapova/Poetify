'''
Created on Apr 10, 2016

@author: Yuliya Astapova
'''

import argparse, sys
sys.path.append('..')
from hw import trainpcfg, parsepcfg


parser = argparse.ArgumentParser(description='Includes the training application ' +
                                 'that induces the PCFG, the CYK Parser, ' + 
                                 'and the Evaluator application.')
parser.add_argument('-train', metavar='train.trees', type=str,
                    help='Induces the PCFG from the file containing the training data.')
parser.add_argument('-parse', metavar=('pcfg.txt', 'test.txt'), type=str, nargs=2,
                    help='Reads the grammar from a file and then parses a list of sentences into a tree.')
parser.add_argument('-all_rules', action='store_true',
                     help="Determines whether or not to use all possible rules in the grammar.")

args = parser.parse_args()
training = args.train
parsing = args.parse
all_rules = args.all_rules

# opens a file and reads it
def read_file(name):
    print('Reading ' + name, flush=True)
    f = open(name, 'r')
    input_file = f.read()
    f.close()
    return(input_file)


# runs the PCFG training
if(training != None):
    print('Beginning training.', flush=True)
    input_file = read_file(training)
    trainpcfg.train(input_file)
    print('Finished training.', flush=True)

# runs the parser on a set of sentences
if(parsing != None):
    print('Reading ' + parsing[0], flush=True)
    u_lhs, tags, rules, probs, ntags, nwords = parsepcfg.parse_grammar(parsing[0])
    print('Finished reading grammar file.', flush=True)
    test_text = read_file(parsing[1])
    print('Finished reading.', flush=True)
    print('Beginning creating trees.', flush=True)
    parsepcfg.create_trees(all_rules, test_text, u_lhs, tags, rules, probs, ntags, nwords)