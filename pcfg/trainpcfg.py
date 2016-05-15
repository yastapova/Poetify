'''
Created on Apr 11, 2016

@author: Yuliya
'''
import sys
sys.path.append('..')

from pcfg import tree

# uses the from_str() function in tree.py
# to read a tree from its string representation
# returns a list of all the trees in the file
def read_trees(input_file):
    tree_list = []
    input_file = input_file.strip()
    input_file = input_file.split('\n')
    
    for i in range(0, len(input_file)):
        t = tree.Tree.from_str(input_file[i])
        tree_list.append(t)
    
    return(tree_list)

# counts the rules used by one tree
# recursive
def count_rules(root, rules, unique_lhs, unique_tags, words):
    rootname = root.__str__()   # root will be a tag
    children = root.children    # can have 1 or 2 children
    
    if rootname.isupper():
        unique_tags[rootname] = 1
    
    if(len(children) <= 0):
        return()    # it is a terminal, so there are no more rules in this branch
    elif(len(children) == 1):   # rule TAG --> terminal
        child0 = children[0].__str__()
        r = (rootname, child0)
        if r in rules:
            rules[r] += 1
        else:
            rules[r] = 1
        if rootname in unique_lhs:
            unique_lhs[rootname] += 1
        else:
            unique_lhs[rootname] = 1
        if not child0.isupper():
            if child0 in words:
                words[child0] += 1
            else:
                words[child0] = 1
        else:
            unique_tags[child0] = 1
        count_rules(children[0], rules, unique_lhs, unique_tags, words)
    elif(len(children) == 2):   # rule TAG1 --> TAG2 TAG3
        child0 = children[0].__str__()
        child1 = children[1].__str__()
        r = (rootname, child0, child1)
        if r in rules:
            rules[r] += 1
        else:
            rules[r] = 1
        if rootname in unique_lhs:
            unique_lhs[rootname] += 1
        else:
            unique_lhs[rootname] = 1
        #childs = child0 + ' ' + child1
        if not child0.isupper():
            if child0 in words:
                words[child0] += 1
            else:
                words[child0] = 1
        else:
            unique_tags[child0] = 1
        if not child1.isupper():
            if child1 in words:
                words[child1] += 1
            else:
                words[child1] = 1
        else:
            unique_tags[child1] = 1
        count_rules(children[0], rules, unique_lhs, unique_tags, words)
        count_rules(children[1], rules, unique_lhs, unique_tags, words)
    else:
        raise Exception('too many children')    # should never happen

def weed_unks(rules, words):
    words['<unk>'] = 0
    unks = []
    delete = {}
    add = {}
    for w in words:
        if words[w] == 1:
            words['<unk>'] += 1
            unks.append(w)
            delete[w] = 1
    for d in delete:
        del words[d]
    delete = {}
    for r in rules:
        if len(r) == 2:
            if r[1] in unks:
                tag = r[0]
                if (tag, '<unk>') not in add:
                    add[(tag, '<unk>')] = 1
                else:
                    add[(tag, '<unk>')] += 1
                delete[r] = 1
    for d in delete:
        del rules[d]
    for a in add:
        rules[a] = add[a]

# counts the rules used by each tree in the list
def count_all_rules(tree_list):
    rules = {}  # dictionary for rules
    u_lhs = {}  # dictionary for unique tags on the LHS and their counts
    u_tags = {} # dictionary for all unique tags
    words = {}  # dictionary for all unique words
    countu = 0  # count of unary rules
    countb = 0  # count of binary rules
    for t in tree_list:
        count_rules(t.root, rules, u_lhs, u_tags, words)
    for r in rules:
        if len(r) == 2:
            countu += 1
        else:
            countb += 1
    print('Unary rules:\t' + str(countu))
    print('Binary rules:\t' + str(countb))
    return(rules, u_lhs, u_tags, words)

# runs through each rule in the rules dictionary,
# calculates its Laplace probability,
# and puts the probability into a new dictionary
def calc_probs(rules, u_lhs, u_tags, words):
    probs = {}
    tags = len(u_tags)
    # rationale for this equation is given in the report
    additionals = len(words) + tags**2
    for r in rules:
        left = r[0]
        rulecount = rules[r]
        leftcount = u_lhs[left]
        denom = leftcount + additionals
        probs[r] = (rulecount + 1)/denom
    return(probs)

# writes all of the info about the grammar to a file
def write_PCFG_file(u_lhs, u_tags, rules, probs, words):
    print('Writing to pcfg.txt', flush=True)
    f = open('pcfg.txt', 'w')
    f.write('Unique LHS:\t' + str(len(u_lhs)) + '\n')
    f.write('Unique Tags:\t' + str(len(u_tags)) + '\n')
    f.write('Unique Terminals:\t' + str(len(words)) + '\n')
    f.write('Num rule counts:\t' + str(len(rules)) + '\n')
    f.write('LHS Counts:\n')
    for x in u_lhs:
        f.write(x + '\t' + str(u_lhs[x]) + '\n')
    f.write('Rule counts, Probabilities:\n')
    for r in rules:
        r0 = r[0]
        r1 = r[1]
        if(len(r) > 2):
            r2 = r[2]
            f.write(r0 + ' ' + r1 + ' ' + r2 + '\t' + str(rules[r]) + ' ' + str(probs[r]) + '\n')
        else:
            f.write(r0 + ' ' + r1 + '\t' + str(rules[r]) + ' ' + str(probs[r]) + '\n')
    f.write('All tags:\n')
    for t in u_tags:
        f.write(t + ' ')
    f.write('\n')
    
    f.close()

# prints the top 10 binary rules
def show_max_10_binary(probs):
    print('Top 10 Most Probable Rules:', flush=True)
    sorted_probs = sorted(probs, key=probs.get, reverse=True)
    count = 0
    for p in sorted_probs:
        if(count == 10):
            break
        if len(p) == 3:
            count += 1
            print(p[0] + ' -> ' + p[1] + ' ' + p[2] + '\t\t' + str(probs[p]), flush=True)

# runs all of the training functions
def train(input_file):
    tree_list = read_trees(input_file)
    rules, u_lhs, u_tags, words = count_all_rules(tree_list)
    weed_unks(rules, words)
    probs = calc_probs(rules, u_lhs, u_tags, words)
    write_PCFG_file(u_lhs, u_tags, rules, probs, words)
    show_max_10_binary(probs)
    