__author__ = 'laceyliu'
# from nltk import tokenize
# from nltk import pos_tag
# s = "What is Delta Cancri also known as?"
# tagged = pos_tag(tokenize.word_tokenize(s))
# print tagged
import re
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
import stanford_utils

import tree_parser
qs = [
    "What is the magnitude of the brightest star in Gemini?",
    "What is the maximum rate of Geminids meteor showers?",
    "What is the magnitude of M35 (NGC 2168)?",
    "What is the length of production cycle of Prisoner of Azkaban?"
]

qs2 = [
    "What was Perl originally named?",
    "What is Delta Cancri also known as?",
    "What did manilius and ovid call the constellation in ancient rome?"
]

qs3 = [
    "What is the three-letter abbreviation for the constellation?",
    "What was the first club Beckham played for?"
       ]
s = [
    "In Ancient Rome, Manilius and Ovid called the constellation Litoreus (shore-inhabiting).",
    "With Prisoner of Azkaban, production of the Harry Potter films switched to an eighteen-month cycle, which producer David Heyman explained was \"to give each [film] the time it required.\"",
    "Perl was originally named \"Pearl\".",
    "Tottenham Hotspur was the first club he played for.",
]
# for q in s:
#     tree = tree_parser.sent_to_tree(q)
#     for t in tree:
#         print(t)

test = "Harry, Ron and Hermione head back to school on the Hogwarts Express. "
ner_tagger = stanford_utils.new_NERtagger()
tagged = ner_tagger.tag(test.split(" "))
parsed = tree_parser.sent_to_tree(test)

def contains_name(tagged_sent):
    for tup in tagged_sent:
        if tup[1] == "PERSON":
            return True
        elif tup[0].lower() == "he" or tup[0].lower() == "she":
            return True
    return False

# get basic form for verb (set pos = 'v' for verb)
def basicForm(word, pos):
    exceptions = wn._exception_map[pos]
    if word in exceptions:
        return exceptions[word][0]
    else:
        return WordNetLemmatizer().lemmatize(word, pos)

def get_who(tree):
    question = "who "
    verbP = re.compile("^V[BP].{0,1}$")
    for node in tree[0]:
        if node.label() != "NP":
            if node.label() == "VP":
                for i in xrange(len(node)):
                    if node[i].label() == "MD":
                        break;
                    elif node[i].label() == "VBZ":
                        if node[i][0] != "is" and not (node[i][0] == "has" and i+1<len(node) and verbP.match(node[i+1].label())):
                            question = "who does" + question[question.find(" "):]
                            for j in xrange(i, len(node)):
                                if node[j].label() == "VBZ":
                                    node[j][0] = basicForm(node[j][0], 'v')
                            break;
                    elif node[i].label() == "VBD":
                        if node[i][0] != "was" and node[i][0] != "were" and not (node[i][0] == "had" and i+1<len(node) and verbP.match(node[i+1].label())):
                            question = "who did" + question[question.find(" "):]
                            for j in xrange(i, len(node)):
                                if node[j].label() == "VBD":
                                    node[j][0] = basicForm(node[j][0], 'v')
            question += " ".join([leave for leave in node.leaves()]) + " "
    question = question[:len(question)-3] + "?"
    return question

print contains_name(tagged)
print get_who(parsed)