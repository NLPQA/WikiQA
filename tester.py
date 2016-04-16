import nltk
import stanford_utils
import tree_parser

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

