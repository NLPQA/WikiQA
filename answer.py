__author__ = 'laceyliu'
import doc_parser
import stanford_utils
import tree_parser
from nltk import Tree
mds = ["did", "do", "does", "di", "do", "doe"]
tagger = stanford_utils.new_NERtagger()
stemmer = doc_parser.stemmer
import nltk.parse
def answer_binary(q, s):
    # print q
    # print s
    q_vect = doc_parser.sent_to_vect(q.lower())
    s_vect = doc_parser.sent_to_vect(s.lower())
    # print q_vect
    # print s_vect
    for token, cnt in q_vect.items():
        if token not in s_vect and token not in mds:
            return "No."
    negs = ["not", "no", "never"]
    for neg in negs:
        if neg in q:
            return "No."
    return "Yes"

def answer_how_many(q, s):
    num = filter(str.isdigit, s)
    return num if len(num) > 0 else "0"

def answer_what(q, s):
    return ""

def answer_who(q, s):
    return ""

def answer_why(q, s):
    return ""

def answer_when(q, s):
    # handles the wh-subject-question: S -> Wh- NP VP
    q_tree = tree_parser.sent_to_tree(q)
    s_tree = tree_parser.sent_to_tree(s)
    q_np, q_vp = get_np_vp(q_tree)
    s_np, s_vp = get_np_vp(s_tree)
    # match head of both VPs
    q_vp_head = get_vp_head(q_vp)
    s_vp_head = get_vp_head(s_vp)
    q_vp_head = stemmer.stem(tree_parser.tree_to_sent(q_vp_head)).encode('ascii', 'ignore')
    s_vp_head = stemmer.stem(tree_parser.tree_to_sent(s_vp_head)).encode('ascii', 'ignore')
    if q_vp_head == s_vp_head:
        ans = tree_parser.tree_to_sent(Tree('S', [s_np, s_vp]))
    else:
        ans = ""
    return ans

def ans_when(q, sents):
    ans = ""
    for sent in sents:
        tagged = nltk.pos_tag(nltk.word_tokenize(sent[0].replace("-", " ")))
        pps = [item for item in tagged if item[1] == "IN"]
        if len(pps) == 0:
            continue
        ans = answer_when(q, sent[0])
        if len(ans) > 0:
            break
    return ans


def answer_where(q, s):
    return ""



# helper functions:
def get_np_vp(tree):
    np = None
    vp = None
    for subtree in tree.subtrees():
        if np is None and subtree.label() == "NP":
            np = subtree
        if vp is None and subtree.label() == "VP":
            vp = subtree
    return np, vp

def get_vp_head(vp):
    for sub in vp.subtrees():
        if sub.label() == "VB" or sub.label() == "VBD":
            return sub


# Yes or No questions
# print answer_binary("Do adjectives come before nouns?",
#                   "In English, adjectives come before the nouns they modify and after determiners.")
# print answer_binary("Was Harry Potter and the Prisoner of Azkaban the first film in the series to be released in both conventional and IMAX theatres?",
#                     "It was the first film in the series to be released in both conventional and IMAX theatres.")


# When questions
# print answer_when("When did John graduate from cmu?", "John graduated from cmu in 1990s.")
