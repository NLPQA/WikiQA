__author__ = 'laceyliu'
import doc_parser
import stanford_utils
import tree_parser
import stanford_utils
from nltk import Tree
import ans_ranker
import nltk
mds = ["did", "do", "does", "di", "do", "doe"]
reps = ["it", "they", "he", "she"]
tagger = stanford_utils.new_NERtagger()
# stemmer = doc_parser.stemmer
from nltk.corpus import wordnet as wn
def answer_which(q, s):
    return ""

def answer_binary(q, sents, title):
    title = title.lower().split(" ")
    q_vect = doc_parser.sent_to_vect(q.lower())
    sent = ans_ranker.rerank_match(q_vect, sents, mds+title)
    s_vect = doc_parser.sent_to_vect(sent.lower())
    negs = ["not", "no", "never"]
    for neg in negs:
        if neg in s_vect:
            return "No.", sent
    return "Yes", sent

def answer_how_many(q, s):
    if "visible stars" in q:
        a = 1
    q_tokens = nltk.tokenize.word_tokenize(q)
    s_tokens = nltk.tokenize.word_tokenize(s)
    target = q_tokens[2]

    t_index = s_tokens.index(target)
    n_index = t_index-1
    while n_index >= 0 and (not str.isdigit( s_tokens[n_index])):
        n_index -= 1

    return s_tokens[n_index] if n_index>=0 else ""
    # num = filter(str.isdigit, s)
    # return num if len(num) > 0 else "0"

def answer_definitions(main_vp, s, verb):
    nps = tree_parser.get_phrases(main_vp, "NP", True, True)
    if len(nps)>0:
        candidates = s.split(" "+verb)
        if tree_parser.tree_to_sent(nps[0]) in candidates[0]:
            ans_tree = tree_parser.sent_to_tree(candidates[1])
        else:
            ans_tree = tree_parser.sent_to_tree(candidates[0])
        s_nps = tree_parser.get_phrases(ans_tree, "NP", True, True)
        if len(s_nps) > 0:
            return tree_parser.tree_to_sent(s_nps[0])
        else:
            return ""

def get_main_verb(vp):
    leaves = vp.leaves()
    return leaves[0]

def quest_to_state(q):
   q = q.replace("?", "")
   tokens = q.split(" ")
   if tokens[0].startswith("Wh"):
       return ' '.join(tokens[2:])
   if tokens[0] == "How" and tokens[1] == "many":
       return ' '.join(tokens[3:])
   return ' '. join(tokens[1:])

def is_definition(q):
    bes = ["is", "are", "am", "were", "was"]
    for be in bes:
        if be in q:
            return True
    return False

def answer_what(q, sents, title):
    title = title.lower().split(" ")
    q_vect = doc_parser.sent_to_vect(q.lower())
    s = ans_ranker.rerank_match(q_vect, sents, mds+title)
    ans = ""
    if not is_definition(q):
        qbody = quest_to_state(q)+"Dog"
    else:
        qbody = q.replace("What", "Dog").replace("?", "")
    s = s.lower()
    parsed_q = tree_parser.sent_to_tree(qbody)
    vps = tree_parser.get_phrases(parsed_q, "VP",True, True)
    main_vp = vps[0]
    main_vb = get_main_verb(main_vp)
    ans = answer_definitions(main_vp, s, main_vb)
    return ans, s

# what_s = "Tom studies computer science at CMU."
# what_q = "What does Tom study at cmu?"
# print answer_what(what_q, what_s)

def answer_who(q, sents, title):
    title = title.lower().split(" ")
    q_vect = doc_parser.sent_to_vect(q.lower())
    s = ans_ranker.rerank_match(q_vect, sents, mds+title)
    ans = ""
    qbody = q.replace("Who", "Doug").replace("?", "")
    s = s.lower()
    parsed_q = tree_parser.sent_to_tree(qbody)
    vps = tree_parser.get_phrases(parsed_q, "VP",True, True)
    main_vp = vps[0]
    main_vb = get_main_verb(main_vp)
    ans = answer_definitions(main_vp, s, main_vb)
    return ans, s
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

def answer_when(q, sents, title):
    title = title.lower().split(" ")
    q_vect = doc_parser.sent_to_vect(q.lower())
    s = ans_ranker.rerank_match(q_vect, sents, mds+title)
    parsed_s = tree_parser.sent_to_tree(s)
    pps = tree_parser.get_phrases(parsed_s, "PP", False, True)
    for pp in pps:
        sent_pp = tree_parser.tree_to_sent(pp)
        tagged_pp = tagger.tag(nltk.tokenize.word_tokenize(sent_pp))
        for tup in tagged_pp:
            if tup[1] == "DATE" or tup[1] == "TIME":
                return sent_pp.strip()+".", s
    tagged_sent = tagger.tag(nltk.tokenize.word_tokenize(s))
    ans = ""
    for i in xrange(0, len(tagged_sent)):
        tup = tagged_sent[i]
        if tup[1] == "DATE" or tup[1] == "TIME":
            j = i
            while tagged_sent[j][1] == "DATE" or tagged_sent[j][1] == "TIME":
                ans += tagged_sent[j][0] + " "
                j += 1
            return ans.strip()+".", s
    return "", s
#
# test_s = "Alexandra \"Alex\" Patricia Morgan Carrasco (born July 2, 1989), ne Alexandra Patricia Morgan, is an American soccer player, Olympic gold medalist, and FIFA Women's World Cup champion."
# test_q = "When was Morgan born?"
# print answer_when(test_q, test_s)

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


def answer_where(q, sents, title):
    title = title.lower().split(" ")
    q_vect = doc_parser.sent_to_vect(q.lower())
    s = ans_ranker.rerank_match(q_vect, sents, mds+title)
    parsed_s = tree_parser.sent_to_tree(s)
    pps = tree_parser.get_phrases(parsed_s, "PP", False, True)
    for pp in pps:
        sent_pp = tree_parser.tree_to_sent(pp)
        tagged_pp = tagger.tag(nltk.tokenize.word_tokenize(sent_pp))
        for tup in tagged_pp:
            if tup[1] == "LOCATION" or tup[1] == "ORGANIZATION":
                return sent_pp.strip()+".", s
    return "", s


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