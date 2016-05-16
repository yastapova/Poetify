# tree.py
# David Chiang <chiang@isi.edu>
# slightly modified by Liang Huang <lhuang@isi.edu> to remove quotes surrounding words.
# 4/10/16 - modified by Yuliya Astapova to change the print to comply with Python3

import re

class RootDeletedException(Exception):
    pass

class Node(object):
    def __init__(self, label, children):
        self.label = label
        self.children = children
        for (i,child) in enumerate(self.children):
            if child.parent is not None:
                child.detach()
            child.parent = self
            child.order = i
        self.parent = None
        self.order = 0

    def __str__(self):
        return self.label

    def _subtree_str(self):
        if len(self.children) != 0:
            return "%s(%s)" % (self.label, " ".join(child._subtree_str() for child in self.children))
        else:
            s = '%s' % self.label
            #s = s.replace("(", "-LRB-")
            #s = s.replace(")", "-RRB-")
            return s
        
    def _subtree_str2(self):
        if len(self.children) != 0:
            return "%s" % (" ".join(child._subtree_str2() for child in self.children))
        else:
            s = '%s' % self.label
            #s = s.replace("(", "-LRB-")
            #s = s.replace(")", "-RRB-")
            return s

    def insert_child(self, i, child):
        if child.parent is not None:
            child.detach()
        child.parent = self
        self.children[i:i] = [child]
        for j in range(i,len(self.children)):
            self.children[j].order = j

    def append_child(self, child):
        if child.parent is not None:
            child.detach()
        child.parent = self
        self.children.append(child)
        child.order = len(self.children)-1

    def delete_child(self, i):
        self.children[i].parent = None
        self.children[i].order = 0
        self.children[i:i+1] = []
        for j in range(i,len(self.children)):
            self.children[j].order = j

    def detach(self):
        if self.parent is None:
            raise RootDeletedException
        self.parent.delete_child(self.order)

    def delete_clean(self):
        "Cleans up childless ancestors"
        parent = self.parent
        self.detach()
        if len(parent.children) == 0:
            parent.delete_clean()

    def bottomup(self):
        for child in self.children:
            for node in child.bottomup():
                yield node
        yield self

    def leaves(self):
        if len(self.children) == 0:
            yield self
        else:
            for child in self.children:
                for leaf in child.leaves():
                    yield leaf

class Tree(object):
    def __init__(self, root):
        self.root = root

    def __str__(self):
        return self.root._subtree_str()
    
    def __str2__(self):
        return self.root._subtree_str2()

    interior_node = re.compile(r"\s*([^\s(]*)\(")
    close_brace = re.compile(r"\s*\)")
    # lhuang: unquote
    leaf_node = re.compile(r'\s*([^\s)]+)')

    @staticmethod
    def _scan_tree(s):
        result = Tree.interior_node.match(s)
        if result != None:
            label = result.group(1)
            pos = result.end()
            children = []
            (child, length) = Tree._scan_tree(s[pos:])
            while child != None:
                children.append(child)
                pos += length
                (child, length) = Tree._scan_tree(s[pos:])
            result = Tree.close_brace.match(s[pos:])
            if result != None:
                pos += result.end()
                return Node(label, children), pos
            else:
                return (None, 0)
        else:
            result = Tree.leaf_node.match(s)
            if result != None:
                pos = result.end()
                label = result.group(1)
                #label = label.replace("-LRB-", "(")
                #label = label.replace("-RRB-", ")")
                return (Node(label,[]), pos)
            else:
                return (None, 0)

    @staticmethod
    def from_str(s):
        s = s.strip()
        (tree, n) = Tree._scan_tree(s)
        return Tree(tree)

    def bottomup(self):
        return self.root.bottomup()

    def leaves(self):
        return self.root.leaves()

    def remove_empty(self):
        nodes = list(self.bottomup())
        for node in nodes:
            if node.label in ["-NONE-", "XXX"]:
                try:
                    node.delete_clean()
                except RootDeletedException:
                    self.root = None

    def remove_unit(self):
        nodes = list(self.bottomup())
        for node in nodes:
            if len(node.children) == 1:
                child = node.children[0]
                if len(child.children) > 0:
                    node.label = "%s_%s" % (node.label, child.label)
                    child.detach()
                    for grandchild in list(child.children):
                        node.append_child(grandchild)

    def binarize_right(self):
        nodes = list(self.bottomup())
        for node in nodes:
            if len(node.children) > 2:
                # create a right-branching structure
                children = list(node.children)
                children.reverse()
                vlabel = node.label+"*"
                prev = children[0]
                for child in children[1:-1]:
                    prev = Node(vlabel, [child, prev])
                node.append_child(prev)

    def binarize_left(self):
        nodes = list(self.bottomup())
        for node in nodes:
            if len(node.children) > 2:
                # create a left-branching structure
                vlabel = node.label+"*"
                children = list(node.children)
                prev = children[0]
                for child in children[1:-1]:
                    prev = Node(vlabel, [prev, child])
                node.insert_child(0, prev)

    def binarize(self):
        nodes = list(self.bottomup())
        for node in nodes:
            if len(node.children) > 2:

                if node.label in ['SQ']:
                    # create a right-branching structure
                    children = list(node.children)
                    children.reverse()
                    vlabel = node.label+"*"
                    prev = children[0]
                    for child in children[1:-1]:
                        prev = Node(vlabel, [child, prev])
                    node.append_child(prev)
                else:
                    # create a left-branching structure
                    vlabel = node.label+"*"
                    children = list(node.children)
                    prev = children[0]
                    for child in children[1:-1]:
                        prev = Node(vlabel, [prev, child])
                    node.insert_child(0, prev)

if __name__ == "__main__":
    import sys
    for line in sys.stdin:
        t = Tree.from_str(line)
        print(t)
        
