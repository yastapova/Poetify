'''
Created on Apr 13, 2016

@author: Yuliya
'''

from math import log

# opens the pcfg file and reconstructs the grammar
def read_PCFG_file(f):
    f = open(f, 'r')
    line = f.readline().split('\t')
    len_u_lhs = int(line[1])
    line = f.readline().split('\t')
    len_u_tags = int(line[1])
    line = f.readline().split('\t')
    len_u_words = int(line[1])
    line = f.readline().split('\t')
    len_rules = int(line[1])
    f.readline()
    
    u_lhs = {}
    for i in range(0, len_u_lhs):
        line = f.readline().split('\t')
        u_lhs[line[0]] = int(line[1])
    
    f.readline()
    rules = {}
    probs = {}
    for i in range(0, len_rules):
        line = f.readline().split('\t')
        r = line[0].split(' ')
        n = line[1].split(' ')
        if len(r) == 2:
            r = (r[0], r[1])
        elif len(r) == 3:
            r = (r[0], r[1], r[2])
        rules[r] = int(n[0])
        probs[r] = float(n[1])
        
    f.readline()
    line = f.readline().rstrip()
    tags = line.split(' ')
    tags = sorted(tags)
    
    f.close()
    return(u_lhs, tags, rules, probs, len_u_tags, len_u_words)

# gets a rule's Laplace probability from the grammar, if it exists
# if not, that means it wasn't observed, so this function
# calculates the Laplace prob on the fly
def get_Laplace_prob(rule, grammar, u_lhs, ntags, nwords):
    if rule in grammar:
        return grammar[rule]
    else:
        if len(rule) == 2:
            rule = (rule[0], '<unk>')
            if rule in grammar:
                return grammar[rule]
            else:
                denom = nwords + ntags**2
                if rule[0] in u_lhs:
                    denom += u_lhs[rule[0]]
                return 1/denom
        else:
            denom = nwords + ntags**2
            if rule[0] in u_lhs:
                denom += u_lhs[rule[0]]
            return 1/denom

# recursively builds the tree from two chosen child rules
def buildTreeRecursive(all_rules, word, tag, row, tags, backs, scores, sent):
    r = scores[row][word]
    max_value = max(r)
    max_index = r.index(max_value)
    bp = backs[row][word][max_index]
    if not all_rules:
        if bp == None:
            return None
    
    if(row == word):
        return tags[tag] + '(' + sent[word] + ')'
    else:
        s1 = buildTreeRecursive(all_rules, bp[0], bp[1], row, tags, backs, scores, sent)
        s2 = buildTreeRecursive(all_rules, word, bp[2], bp[0]+1, tags, backs, scores, sent)
        
        if not all_rules:
            if s1 == None or s2 == None:
                return None
        
        s = tags[tag] + '('
        s = s + s1
        s = s + ' ' + s2
        s = s + ')'
        return s

# begins building the parse tree
# starts with the top right corner of the array
def buildTree(all_rules, scores, backs, tags, sent):
    print('Beginning tree creation.', flush=True)
    last = len(backs)
    last = scores[0][last-1]
    top = tags.index('TOP')
    bp = backs[0][len(backs)-1]
    print(bp)
    bp = max(x for x in bp if x is not None)
    print(bp)
    
    if not all_rules:
        if bp == None:
            return "Sentence cannot be parsed."

    word = bp[0]
    t1 = bp[1]
    t2 = bp[2]
    
    s1 = buildTreeRecursive(all_rules, word, t1, 0, tags, backs, scores, sent)
    s2 = buildTreeRecursive(all_rules, len(backs)-1, t2, word+1, tags, backs, scores, sent)
    
    if not all_rules:
        if s1 == None or s2 == None:
            return "Sentence cannot be parsed."
    
    s = tags[top] + '('
    s = s + s1
    s = s + ' ' + s2
    s = s + ')'
    return s

def CKY(all_rules, sent, grammar, u_lhs, tags, ntags, nwords):
    scores = [[[-100000000 for k in range(0, ntags)] for j in range(0, len(sent))] for i in range(0, len(sent))]
    backs = [[[None for k in range(0, ntags)] for j in range(0, len(sent))] for i in range(0, len(sent))]
    
    # fills in the diagonal of the array,
    # which corresponds to the terminals/words of the sentence
    print('Doing unary rules.', flush=True)
    for w in range(0, len(sent)):
        # sets probabilities for POS tags for each word
        for t in range(0, len(tags)):
            scores[w][w][t] = log(get_Laplace_prob((tags[t], sent[w]), grammar, u_lhs, ntags, nwords))
            backs[w][w][t] = [w]

    print('Done with unary rules.', flush=True)
    print('Beginning binary rules.', flush=True)
    
    # starts to fill in the spots above the diagonal.
    # if you think about span = 1 being the diagonal,
    # span = 2 is then the next diagonal up, and so on
    for span in range(2, len(sent) + 1):
        print('[Progress] ' + str(span/(len(sent) + 1)*100) + '%', flush=True)
        for begin in range(0, len(sent) - span + 1):
            end = begin + span - 1
            for split in range(begin, end):
                for r in ((x,y,z) for x in tags for y in tags for z in tags):
                    # if all_rules is False, this makes sure that
                    # rules are only used if they occurred in the training set
                    if not all_rules:
                        if r not in grammar:
                            continue
                    p1 = scores[begin][split][tags.index(r[1])]
                    p2 = scores[split+1][end][tags.index(r[2])]
                    p3 = get_Laplace_prob(r, grammar, u_lhs, ntags, nwords)
                    
                    p = p1 + p2 + log(p3)
                    if p > scores[begin][end][tags.index(r[0])]:
                        scores[begin][end][tags.index(r[0])] = p
                        # set pointer to what rules you go to from here
                        backs[begin][end][tags.index(r[0])] = [split, tags.index(r[1]), tags.index(r[2])]
    print('Done with binary rules.', flush=True)
    
    # builds the tree
    return buildTree(all_rules, scores, backs, tags, sent)

# parses the grammar file 
def parse_grammar(input_file):
    u_lhs, tags, rules, probs, ntags, nwords = read_PCFG_file(input_file)
    return u_lhs, tags, rules, probs, ntags, nwords
    
# runs the tree creation
def create_trees(all_rules, test_text, u_lhs, tags, rules, probs, ntags, nwords):
    test_text = test_text.strip().split('\n')
    f = open('parse.trees', 'w')
    for t in range(0, len(test_text)):
        test_text[t] = test_text[t].strip().split(' ')
    test_text = test_text[len(test_text)-2:]
    for s in test_text:
        print('Working on sentence ' + str(s) + '.', flush=True)
        s_parse = CKY(all_rules, s, probs, u_lhs, tags, ntags, nwords)
        f.write(s_parse + '\n')
        f.flush()
        print(s_parse)
    f.close()