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
    if tree == None:
        return ""
    return ' '.join(tree.leaves())

def get_phrases(tree, pattern, reversed, sort):
    phrases = []
    for t in tree.subtrees():
        if t.label() == pattern:
            phrases.append(t)
    if sort == True:
        phrases = sorted(phrases, key=lambda x:len(x.leaves()), reverse=reversed)
    return phrases

# # test = 'Perl was originally named "Pearl".'
# # test_tree = sent_to_tree(test)
# # # traverse(test_tree)
# # # test_sent = tree_to_sent(test_tree)
# # # print test_tree
# # # print test_sent
# #
# # test = "Clinton Drew, born on March 9, 1983, is an American soccer player who plays for Tottenham Hotspur and the United States national team."
# # tree = sent_to_tree(test)
# # vplist = get_phrases(tree, "VP")
# # pplist = get_phrases(tree, "PP")
# # nplist = get_phrases(tree, "NP")
#
# # for vp in vplist:
# #     print vp
# for np in nplist:
#     print np
