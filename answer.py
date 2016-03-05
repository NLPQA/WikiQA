__author__ = 'laceyliu'
import doc_parser
import stanford_utils
mds = ["did", "do", "does", "di", "do", "doe"]
tagger = stanford_utils.new_NERtagger()

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
    return ""
def answer_where(q, s):
    return ""

print answer_how_many('111', 'test 12 taest 12')