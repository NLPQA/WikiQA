__author__ = 'laceyliu'
import stanford_utils
import tree_parser
import nltk
mds = ["did", "do", "does", "di", "do", "doe"]
reps = ["it", "they", "he", "she"]
tagger = stanford_utils.new_NERtagger()
from nltk.corpus import wordnet as wn

def answer_which(q, s):
    return ""

def answer_binary(sent, miss):
    s_vect = sent.split(" ")
    if miss >= 2:
        return "No."
    negs = ["not", "no", "never"]
    for neg in negs:
        if neg in s_vect:
            return "No."
    return "Yes"

def answer_how_many(q, s):
    q_tokens = nltk.tokenize.word_tokenize(q)
    s_tokens = nltk.tokenize.word_tokenize(s)
    target = q_tokens[2]

    t_index = s_tokens.index(target)
    n_index = t_index-1
    while n_index >= 0 and (not str.isdigit(s_tokens[n_index])):
        n_index -= 1

    return s_tokens[n_index] if n_index>=0 else ""
    # num = filter(str.isdigit, s)
    # return num if len(num) > 0 else "0"

def answer_non_definitions(main_vp, s, verb):
    nps = tree_parser.get_phrases(main_vp, "NP", False, False)
    if len(nps)>0:
        candidates = s.split(" "+verb)
        if tree_parser.tree_to_sent(nps[0]) in candidates[0]:
            ans_tree = tree_parser.sent_to_tree(candidates[1])
        else:
            ans_tree = tree_parser.sent_to_tree(candidates[0])
        s_nps = tree_parser.get_phrases(ans_tree, "NP", False, False)
        if len(s_nps) > 0:
            return tree_parser.tree_to_sent(s_nps[0])
        else:
            return ""

def is_overlap(s1, s2):
    t1 = s1.split(" ")
    t2 = s2.split(" ")
    if len(t2) < len(t1):
        return False

    overlap = 0
    for t in t1:
        if t in t2:
            overlap += 1
    return overlap >= len(t1)-2

def answer_definitions(s, main_nps):
    if len(main_nps) == 0:
        return ""
    main_np = tree_parser.tree_to_sent(main_nps[0])
    parsed_s = tree_parser.sent_to_tree(s)
    vps = tree_parser.get_phrases(parsed_s, "VP", True, True)
    if len(vps) > 0:
        main_vp = vps[0]
    else:
        return ""

    verb = get_main_verb(main_vp)

    candidates = s.split(" "+verb)

    if len(candidates) > 1:
        # if main_np in candidates[1]:
        if is_overlap(main_np, candidates[1]):
            ans_tree = tree_parser.sent_to_tree(candidates[0])
            s_nps = tree_parser.get_phrases(ans_tree, "NP", True, False)
            if len(s_nps) > 0:
                return tree_parser.tree_to_sent(s_nps[0])
            else:
                return candidates[0]
        else:
            ans_tree = tree_parser.sent_to_tree(candidates[1])
            s_nps = tree_parser.get_phrases(ans_tree, "NP", True, False)
            if len(s_nps) > 0:
                return tree_parser.tree_to_sent(s_nps[0])
            else:
                return candidates[1]
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
    bes = [" is", " are", " am", " were", " was"]
    for be in bes:
        if be in q:
            return True
    return False

def answer_what(q, s):
    if "three-letter abbreviation" in q:
        a = 1
    ans = ""

    if is_definition(q):
        qbody = quest_to_state(q)+" is dog"
    else:
        qbody = q.replace("What", "Dog").replace("?", "")
    s = s.lower()
    parsed_q = tree_parser.sent_to_tree(qbody)
    main_nps = tree_parser.get_phrases(parsed_q, "NP", True, True)
    ans = answer_definitions(s, main_nps)
    # if is_definition(q):
    #     qbody = quest_to_state(q)+" is dog"
    #     s = s.lower()
    #     parsed_q = tree_parser.sent_to_tree(qbody)
    #     main_nps = tree_parser.get_phrases(parsed_q, "NP", True, True)
    #     ans = answer_definitions(s, main_nps)
    # else:
    #     qbody = q.replace("What", "Dog").replace("?", "")
    #     s = s.lower()
    #     parsed_q = tree_parser.sent_to_tree(qbody)
    #     vps = tree_parser.get_phrases(parsed_q, "VP",True, True)
    #     main_vp = vps[0]
    #     main_vb = get_main_verb(main_vp)
    #     ans = answer_non_definitions(main_vp, s, main_vb)
    return ans

# what_s = "Tom studies computer science at CMU."
# what_q = "What does Tom study at cmu?"
# print answer_what(what_q, what_s)

def answer_who(q, s):
    ans = ""
    qbody = q.replace("Who", "Doug").replace("?", "")
    s = s.lower()
    parsed_q = tree_parser.sent_to_tree(qbody)
    vps = tree_parser.get_phrases(parsed_q, "VP",True, True)
    main_vp = vps[0]
    main_vb = get_main_verb(main_vp)
    ans = answer_non_definitions(main_vp, s, main_vb)
    return ans
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
    return ans[:-1].strip()+"."

def answer_when(s):
    parsed_s = tree_parser.sent_to_tree(s)
    pps = tree_parser.get_phrases(parsed_s, "PP", False, True)
    for pp in pps:
        sent_pp = tree_parser.tree_to_sent(pp)
        tagged_pp = tagger.tag(nltk.tokenize.word_tokenize(sent_pp))
        for tup in tagged_pp:
            if tup[1] == "DATE" or tup[1] == "TIME":
                return sent_pp.strip()+"."
    tagged_sent = tagger.tag(nltk.tokenize.word_tokenize(s))
    ans = ""
    for i in xrange(0, len(tagged_sent)):
        tup = tagged_sent[i]
        if tup[1] == "DATE" or tup[1] == "TIME":
            j = i
            while tagged_sent[j][1] == "DATE" or tagged_sent[j][1] == "TIME":
                ans += tagged_sent[j][0] + " "
                j += 1
            return ans.strip()+"."
    return ""

def answer_where(s):
    parsed_s = tree_parser.sent_to_tree(s)
    pps = tree_parser.get_phrases(parsed_s, "PP", False, True)
    for pp in pps:
        sent_pp = tree_parser.tree_to_sent(pp)
        tagged_pp = tagger.tag(nltk.tokenize.word_tokenize(sent_pp))
        for tup in tagged_pp:
            if tup[1] == "LOCATION" or tup[1] == "ORGANIZATION":
                return sent_pp.strip()+"."
    return ""


def stem(word):
    return wn.morphy(word).encode('ascii', 'ignore')
