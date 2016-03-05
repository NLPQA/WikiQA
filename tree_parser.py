__author__ = 'laceyliu'
import stanford_utils
from nltk import Tree
parser = stanford_utils.new_parser()

def sents_to_trees(sentences):
    return parser.raw_parse_sents(sentences)

def sent_to_tree(sentence):
    t = parser.raw_parse(sentence)
    return Tree(t,list(t))

def tree_to_sent(tree):
    return ' '.join(tree.leaves())



test = 'Perl was originally named "Pearl".'
test_tree = sent_to_tree(test)
# traverse(test_tree)
# test_sent = tree_to_sent(test_tree)
# print test_tree
# print test_sent