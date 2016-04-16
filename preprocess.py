__author__ = 'yitinghao'

from nltk.tree import *
from nltk.draw import tree
import nltk

# Remove parts we don't want
def remove(parent, component):
    for node in parent:
        if type(node) is nltk.Tree:
            if node.label() == component:
                parent.remove(node)
            else:
                remove(node, component)

# Split sentences

<<<<<<< HEAD
def removeParts(tree):
    # remove part that tagged with "PRN"
    remove(tree, "PRN")
    # remove part that tagged with "FRAG"
    remove(tree, "FRAG")
    # tree.draw()

