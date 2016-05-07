'''
04/18/2016: Modified by Yuliya Astapova to comply with Python3,
            also print accuracy, and account for different lengths
            of parsefiles and goldfiles.
'''

import sys
sys.path.append('..')
import itertools, collections
from hw import tree

try:
    _, parsefilename, goldfilename = sys.argv
except:
    sys.stderr.write("usage: evalb.py <parse-file> <gold-file>\n")
    sys.exit(1)

def _brackets_helper(node, i, result):
    i0 = i
    if len(node.children) > 0:
        for child in node.children:
            i = _brackets_helper(child, i, result)
        j0 = i
        if len(node.children[0].children) > 0: # don't count preterminals
            result[node.label, i0, j0] += 1
    else:
        j0 = i0 + 1
    return j0

def brackets(t):
    result = collections.defaultdict(int)
    _brackets_helper(t.root, 0, result)
    return result

matchcount = parsecount = goldcount = 0

for parseline, goldline in itertools.zip_longest(open(parsefilename), open(goldfilename)):
    if(goldline != None):
        gold = tree.Tree.from_str(goldline)
        goldbrackets = brackets(gold)
        goldcount += len(goldbrackets)

    if parseline != None and parseline.strip() == "0":
        continue
    
    if(parseline != None):
        parse = tree.Tree.from_str(parseline)
        parsebrackets = brackets(parse)
        parsecount += len(parsebrackets)

    if(parseline != None and goldline != None):
        for bracket,count in iter(parsebrackets.items()):
            matchcount += min(count,goldbrackets[bracket])

print("%s\t%d brackets" % (parsefilename, parsecount))
print("%s\t%d brackets" % (goldfilename, goldcount))
print("matching\t%d brackets" % matchcount)
print("accuracy:\t" + str(matchcount/parsecount*100) + "%")

