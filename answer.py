__author__ = 'laceyliu'
import doc_parser

mds = ["did", "do", "does", "di", "do", "doe"]
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
    return ""
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
