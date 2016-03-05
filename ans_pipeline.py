__author__ = 'laceyliu'

import sys
import doc_parser
from nltk import tokenize
import ans_ranker

# wiki_path, question_path = sys.argv[1], sys.argv[2]

wiki_path, question_path = "test_wiki.htm", "test_quests.txt"

sents = doc_parser.doc_to_sents(wiki_path)
sent_vects = doc_parser.doc_to_vects(wiki_path)
sent_idfs = doc_parser.doc_to_idfs(wiki_path)

with  open(question_path) as f:
    quests = f.read().splitlines()

for q in quests:
    q_vect = doc_parser.sent_to_vect(q)
    ranked_sents = ans_ranker.rank_sents(q_vect, sents, sent_vects, sent_idfs)
    best = ranked_sents[0][0]
    print q
    print best