import re
import nltk
import stanford_utils
import tree_parser
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn

ner_tagger = stanford_utils.new_NERtagger()
sent = "The Second World War happens from 1953 to 1962."
# sent = "I will have classes on Tuesday and Thursday"
# sent = "I will have breakfast at home"
sent_tokens = nltk.word_tokenize(sent)
pos_sent = nltk.pos_tag(sent_tokens)
ner_sent = ner_tagger.tag(sent_tokens)
parsed_sent = tree_parser.sent_to_tree(sent)

print pos_sent[:]
print ner_sent
parsed_sent.draw()

def get_when(tree):
    question = ""

    return question

print get_when(parsed_sent)


def basicForm(word, pos):
    exceptions = wn._exception_map[pos]
    if word in exceptions:
        return exceptions[word][0]
    else:
        return WordNetLemmatizer().lemmatize(word, pos)

parser = stanford_utils.new_parser()

text = []
# sent = "He was told that Alice would never come back again."
# sent = "He was doing homework."
# sent = "He was accepted by Carnegie Mellon University."
# sent = "He saw her."
# sent = "He buys and eats breakfast."
# sent = "He was here."
# sent = "He has been working on this project whole day."
# sent = "He eats breakfast."
# sent = "He can fly."
# sent = "He should have done this."
# sent = "He happily accepts and signs the offer."
# sent = "David Robert Joseph Beckham is an English former professional footballer."
# sent = "We see the dog running."
# sent = "Tom is eating breakfast."
# sent = "Known for his range of passing, crossing ability and bending free-kicks, he was twice runner-up for FIFA World Player of the Year and in 2004 he was named in the FIFA 100 list of the world's greatest living players."
sent = 'It was one of the 48 constellations described by the 2nd century AD astronomer Ptolemy and it remains one of the 88 modern constellations today.'
t = parser.raw_parse(sent).next()
# print t
# t.draw()

def get_who(tree):
    question = "what "
    verbP = re.compile("^V[BP].{0,1}$")
    for node in tree[0]:
        if node.label() != "NP":
            if node.label() == "VP":
                for i in xrange(len(node)):
                    if node[i].label() == "MD":
                        break;
                    elif node[i].label() == "VBZ":
                        if node[i][0] != "is" and not (node[i][0] == "has" and i+1<len(node) and verbP.match(node[i+1].label())):
                            question = "what does" + question[question.find(" "):]
                            for j in xrange(i, len(node)):
                                if node[j].label() == "VBZ":
                                    node[j][0] = basicForm(node[j][0], 'v')
                            break;
                    elif node[i].label() == "VBD":
                        if node[i][0] != "was" and node[i][0] != "were" and not (node[i][0] == "had" and i+1<len(node) and verbP.match(node[i+1].label())):
                            question = "what did" + question[question.find(" "):]
                            for j in xrange(i, len(node)):
                                if node[j].label() == "VBD":
                                    node[j][0] = basicForm(node[j][0], 'v')
            question += " ".join([leave for leave in node.leaves()]) + " "
    question = question[:len(question)-3] + "?"
    return question

print get_who(t)
# words = ["had", "went", "gave", "going", "dating", "using", "telling", "stepped", "saw"]
# exceptions = wn._exception_map['v']
# print wn._morphy('saw', pos='v')[1]
# for word in words:
#     print basicForm(word, 'v')

# verbP = re.compile("^VB.{0,1}$")
# if verbP.match("VB"):
#     print "True"
# else:
#     print "False"
