__author__ = 'laceyliu'
import re
import stanford_utils
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
import tree_parser
bes = ["am", "are", "was", "were", "have", "has", "is"]

# get basic form for verb (set pos = 'v' for verb)
def basicForm(word, pos):
    exceptions = wn._exception_map[pos]
    if word in exceptions:
        return exceptions[word][0]
    else:
        return WordNetLemmatizer().lemmatize(word, pos)

ner_tagger = stanford_utils.new_NERtagger()

def get_howmany(tree):
    num = ""
    obj = ""
    question = get_binary(tree)
    nps = tree_parser.get_phrases(tree, "NP")

    for np in nps:
        for i in xrange(len(np)):
            if i+1 < len(np) and np[i].label() == "CD" and np[i+1].label() == "NNS":
                num = " ".join(np[i].leaves())
                obj = " ".join(np[i+1].leaves())
                break
        if len(num) > 0 and len(obj)>0:
            break
    return "How many "+obj+ " "+question.replace(num+" ", "").replace(obj, "").strip().rstrip(',').rstrip('.') +"?"


def get_where(tree):
    where = ""
    question = get_binary(tree)
    pps = tree_parser.get_phrases(tree, "PP")
    for pp in pps:
        ner_pp = ner_tagger.tag(pp.leaves())
        for (word, tag) in ner_pp:
            if tag == "LOCATION" or tag == "ORGANIZATION":
                where = " ".join(pp.leaves())
                break
    return "where "+question.replace(where, "").strip().rstrip(',').rstrip('.') +"?"

def get_when(tree):
    when = ""
    question = get_binary(tree)
    pps = tree_parser.get_phrases(tree, "PP", sort=True, reversed = True)
    for pp in pps:
        ner_pp = ner_tagger.tag(pp.leaves())
        for (word, tag) in ner_pp:
            if tag == "TIME" or tag == "DATE":
                when = " ".join(pp.leaves())
                break
    return "when "+question.replace(when, "").rstrip(',').rstrip('.') + "?"

def get_binary(tree):
    question = ""
    verbP = re.compile("^V[BP].{0,1}$")
    md = ""
    mbody = ""

    for node in tree:
        if node.label() == "NP" and len(mbody) == 0:
            for sub in node:
                if sub.label() == "DT" or sub.label() == "PRP" or sub.label() == "IN":
                    first = " ".join(sub.leaves()).lower()
                    if first == "i":
                        first = first.upper()
                    mbody += first
                else:
                    mbody += " "+ " ".join(sub.leaves())
            mbody += " "
            # mbody = " ".join([leave.lower() if node.label() == "DT" else leave for leave in node.leaves()])+" "
        elif node.label() == "VP":
            for i in xrange(len(node)):
                if node[i].label() == "MD" or (node[i][0] in bes):
                # if node[i].label() == "MD" or node[i][0] == "is" or (node[i][0] == "has" and i+1<len(node) and verbP.match(node[i+1].label())):
                    md = " ".join(node[i].leaves())
                    question = md + mbody + question[question.find(" "):]
                    break
                elif node[i].label() == "VBZ":
                    question = "does " + mbody.lstrip() + question[question.find(" "):]
                    for j in xrange(i, len(node)):
                        if node[j].label() == "VBZ":
                            node[j][0] = basicForm(node[j][0], 'v')
                    break
                elif node[i].label() == "VBP":
                    question = "do "  + mbody.lstrip() +  question[question.find(" "):]
                    for j in xrange(i, len(node)):
                        if node[j].label() == "VBD":
                            node[j][0] = basicForm(node[j][0], 'v')
                elif node[i].label() == "VBD":
                    if node[i][0] != "was" and node[i][0] != "were" and not (node[i][0] == "had" and i+1<len(node) and verbP.match(node[i+1].label())):
                        question = "did "  + mbody.lstrip() + " " +question[question.find(" "):]
                        for j in xrange(i, len(node)):
                            if node[j].label() == "VBD":
                                node[j][0] = basicForm(node[j][0], 'v')
            if md != "":
                question += " ".join([leave for leave in node.leaves()]).replace(md, "")
            else:
                question += " ".join([leave for leave in node.leaves()])
    return question.rstrip(',').rstrip('.')

# generate who question
def get_who(tree):
    question = "who "
    verbP = re.compile("^V[BP].{0,1}$")
    for node in tree:
        if node.label() != "NP":
            if node.label() == "VP":
                for i in xrange(len(node)):
                    if node[i].label() == "MD" or (node[i][0] in bes ):
                        break
                    elif node[i].label() == "VBZ":
                        # if node[i][0] != "is" and not (node[i][0] == "has" and i+1<len(node) and verbP.match(node[i+1].label())):
                        question = "who" + question[question.find(" "):]
                            # for j in xrange(i, len(node)):
                                # if node[j].label() == "VBZ":
                                #     node[j][0] = basicForm(node[j][0], 'v')
                        break
                    elif node[i].label() == "VBD":
                        if node[i][0] != "was" and node[i][0] != "were" and not (node[i][0] == "had" and i+1<len(node) and verbP.match(node[i+1].label())):
                            question = "who" + question[question.find(" "):]
                            # for j in xrange(i, len(node)):
                                # if node[j].label() == "VBD":
                                #     node[j][0] = basicForm(node[j][0], 'v')
            question += " ".join([leave for leave in node.leaves()]) + " "
    question = question[:len(question)-3]
    return question.rstrip(',').rstrip('.') + "?"

# generate what question
def get_what(tree):
    question = "what "
    verbP = re.compile("^V[BP].{0,1}$")
    for node in tree:
        if node.label() != "NP":
            if node.label() == "VP":
                for i in xrange(len(node)):
                    if node[i].label() == "MD" or (node[i][0] in bes ):
                        break
                    elif node[i].label() == "VBZ":
                        #if node[i][0] != "is" and not (node[i][0] == "has" and i+1<len(node) and verbP.match(node[i+1].label())):
                        question = "what" + question[question.find(" "):]
                            # for j in xrange(i, len(node)):
                            #     if node[j].label() == "VBZ":
                            #         node[j][0] = basicForm(node[j][0], 'v')
                            # break
                        break
                    elif node[i].label() == "VBD":
                        if node[i][0] != "was" and node[i][0] != "were" and not (node[i][0] == "had" and i+1<len(node) and verbP.match(node[i+1].label())):
                            question = "what" + question[question.find(" "):]
                            # for j in xrange(i, len(node)):
                            #     if node[j].label() == "VBD":
                            #         node[j][0] = basicForm(node[j][0], 'v')
            question += " ".join([leave for leave in node.leaves()]) + " "
    question = question[:len(question)-3]
    return question.rstrip(',').rstrip('.') + "?"
#
# import tree_parser
# test = "the 2nd century AD astronomer Ptolemy described 48 constellations."
# tree = tree_parser.sent_to_tree(test)
# print get_howmany(tree)
