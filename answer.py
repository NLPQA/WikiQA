__author__ = 'laceyliu'
import doc_parser
import stanford_utils
import tree_parser
import stanford_utils
from nltk import Tree
import ans_ranker
import nltk
mds = ["did", "do", "does", "di", "do", "doe"]
tagger = stanford_utils.new_NERtagger()
# stemmer = doc_parser.stemmer
from nltk.corpus import wordnet as wn
def answer_which(q, s):
    return ""

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
    print s
    s = s.lower()
    q = q.replace("What", "Dog").replace("?", ".")
    parsed_q = tree_parser.sent_to_tree(q)
    if "is" in s :
        main_vp = tree_parser.get_phrases(parsed_q, "VP",True, True)
        nps = tree_parser.get_phrases(main_vp[0], "NP", True, True)
        if len(nps)>0:
            candidates = s.split("is")
            if tree_parser.tree_to_sent(nps[0]) in candidates[0]:
                return candidates[1]
            else:
                return candidates[0]
    elif "are" in s :
        main_vp = tree_parser.get_phrases(parsed_q, "VP",True, True)
        nps = tree_parser.get_phrases(main_vp[0], "NP", True, True)
        if len(nps)>0:
            candidates = s.split("are")
            if tree_parser.tree_to_sent(nps[0]) in candidates[0]:
                return candidates[1]
            else:
                return candidates[0]
    else:
        main_vp = tree_parser.get_phrases(parsed_q, "VP",True, True)
        parsed_s = tree_parser.sent_to_tree(s)
        vps = tree_parser.get_phrases(parsed_s,"VP",  True, True)
        if main_vp in vps:
            nps = tree_parser.get_phrases(main_vp, "NP", True, True)
        else:
            nps = tree_parser.get_phrases(parsed_s, "NP", True, False)
    if len(nps) > 0:
        return tree_parser.tree_to_sent(nps[0])
    return ""

def answer_who(q, s):
    q = q.replace("What", "Doug")
    parsed_q = tree_parser.sent_to_tree(q)
    main_vp = tree_parser.get_phrases( parsed_q, "VP",True, True)
    parsed_s = tree_parser.sent_to_tree(s)
    vps = tree_parser.get_phrases(parsed_s,"VP",  True, True)
    if main_vp in vps:
        nps = tree_parser.get_phrases(main_vp, "NP", True, True)
    else:
        nps = tree_parser.get_phrases(parsed_s, "NP", True, False)
    if len(nps)>0:
        return tree_parser.tree_to_sent(nps[0])
    return ""
    # tagged_s = tagger.tag(s.split(" "))
    #
    # persons = []
    # for tuple in tagged_s:
    #     if tuple[1] == "PERSON":
    #         persons.append(tuple[0])
    # if len(persons) == 1:
    #     return persons[0]
    #
    # return ""

def answer_why(q, s):
    s_tokens = nltk.word_tokenize((s.lower()))
    ans = ""
    if "because" in s_tokens:
        ans = " ".join(s_tokens[s_tokens.index("because"):][1:])
    elif "since" in s_tokens:
        ans = " ".join(s_tokens[s_tokens.index("since"):][1:])
    elif "therefore" in s_tokens:
        ans = " ".join(s_tokens[:s_tokens.index("therefore")][1:])
    elif "so" in s_tokens:
        ans = " ".join(s_tokens[:s_tokens.index("so")][1:])
    elif "as" in s_tokens:
        ans = " ".join(s_tokens[s_tokens.index("as"):][1:])
    elif "due to" in s:
        reason_token = s_tokens[s_tokens.index("due"):]
        reason_token = reason_token[1:]
        if "," in reason_token:
            reason_token = reason_token[:s_tokens.index(",")]
        ans = " ".join(reason_token)
    elif "in order to" in s:
        reason_token = s_tokens[s_tokens.index("order"):]
        reason_token = reason_token[1:]
        if "," in reason_token:
            reason_token = reason_token[:s_tokens.index(",")]
        ans = " ".join(reason_token)
    return ans

def answer_when(q, s):
    parsed_s = tree_parser.sent_to_tree(s)
    pps = tree_parser.get_phrases(parsed_s, "PP", False, True)
    for pp in pps:
        sent_pp = tree_parser.tree_to_sent(pp)
        tagged_pp = tagger.tag(nltk.tokenize.word_tokenize(sent_pp))
        for tup in tagged_pp:
            if tup[1] == "DATE" or tup[1] == "TIME":
                return sent_pp+"."
    return ""

# def answer_when(q, s):
#     # handles the wh-subject-question: S -> Wh- NP VP
#     q_tree = tree_parser.sent_to_tree(q)
#     s_tree = tree_parser.sent_to_tree(s)
#     # print s_tree
#     q_np, q_vp = get_question_np_vp(q_tree)  # assume question has only one top level np, one vp.
#     q_vp_head_tree = get_vp_head(q_vp)
#     print "Question main verb:", tree_parser.tree_to_sent(q_vp_head_tree)
#     s_vp_list = extract_vps(s_tree, match_vp_head=tree_parser.tree_to_sent(q_vp_head_tree))  # extract matching vp
#     if len(s_vp_list) > 1:
#         print "We got multiple VP. Chose the first one."
#     ans = tree_parser.tree_to_sent(Tree('S', [q_np, extract_pp(s_vp_list[0])]))+"."
#     return ans.capitalize()


def answer_where(q, s):
    parsed_s = tree_parser.sent_to_tree(s)
    pps = tree_parser.get_phrases(parsed_s, "PP", False, True)
    for pp in pps:
        sent_pp = tree_parser.tree_to_sent(pp)
        tagged_pp = tagger.tag(nltk.tokenize.word_tokenize(sent_pp))
        for tup in tagged_pp:
            if tup[1] == "LOCATION" or tup[1] == "ORGANIZATION":
                return sent_pp+"."
    return ""


# helper functions:
# get_np_vp: Extract top level NP, VP



def stem(word):
    return wn.morphy(word).encode('ascii', 'ignore')
    #return stemmer.stem(word).encode('ascii', 'ignore')
#
# def get_question_np_vp(tree):
#     np = None
#     vp = None
#     for subtree in tree.subtrees():
#         if np is None and subtree.label() == "NP":
#             np = subtree
#         if vp is None and subtree.label() == "VP":
#             vp = subtree
#     return np, vp
#
# def extract_vps(tree, match_vp_head=None):
#     vps = []
#     for subtree in tree.subtrees():
#         if subtree.label() == "VP":
#             if match_vp_head is not None:
#                 for child in subtree:
#                     if child.label().startswith("VB") and stem(tree_parser.tree_to_sent(child)) == stem(match_vp_head):
#                         vps += [subtree]
#             else:
#                 vps += [subtree]
#     assert(len(vps) > 0)
#     return Tree("VP", vps)
#
# def get_vp_head(vp):
#     for sub in vp:
#         if sub.label().startswith("VB"):
#             return sub
#     return None
#
# def extract_pp(vp):
#     print "Extracting PP from (", tree_parser.tree_to_sent(vp), ") ..."
#     print vp
#     sub_trees = []
#     for sub in vp:
#         #if sub.label().startswith("VB"):
#         #     sub_trees += [sub]
#         if sub.label() == "PP":  # optimize this branch.
#             sub_trees += [sub]
#     return Tree('PP', sub_trees)


# Yes or No questions
# print answer_binary("Do adjectives come before nouns?",
#                   "In English, adjectives come before the nouns they modify and after determiners.")
# print answer_binary("Was Harry Potter and the Prisoner of Azkaban the first film in the series to be released in both conventional and IMAX theatres?",
#                     "It was the first film in the series to be released in both conventional and IMAX theatres.")

#tests
# def test():
#     count = 0
#     for line in open("data/question_sent_pair"):
#         count += 1
#         if line.startswith("Where"):
#             q = line.split("?")[0]
#             sent = line.split("?")[1]
#             print "Question:", q+"?"
#             print answer_where(q, sent)
#             print
#
# test()

# tree = tree_parser.sent_to_tree(test)
# for t in tree:
#     print t
# vps = extract_vps(tree)
# print tree_parser.tree_to_sent(vps)