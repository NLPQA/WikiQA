__author__ = 'laceyliu'

import sys
import doc_parser
from nltk import tokenize
import ans_ranker
import answer

# wiki_path, question_path = sys.argv[1], sys.argv[2]

wiki_path, question_path = "test_wiki.htm", "test_quests.txt"

sents = doc_parser.doc_to_sents(wiki_path)
sent_vects = doc_parser.doc_to_vects(wiki_path)
sent_idfs = doc_parser.doc_to_idfs(wiki_path)
quests = []
with  open(question_path) as f:
    quests = f.read().splitlines()
answers = []
for q in quests:
    q_vect = doc_parser.sent_to_vect(q)
    ranked_sents = ans_ranker.rank_sents(q_vect, sents, sent_vects, sent_idfs)
    best = ranked_sents[0][0]
    q_tokens = tokenize.word_tokenize(q)
    ans = ""
    if q_tokens[0] == 'What':
        ans = answer.answer_what(q, best)
    elif q_tokens[0] == 'Who':
        ans = answer.answer_who(q, best)
    elif q_tokens[0] == 'Why':
        ans = answer.answer_why(q, best)
    elif q_tokens[0] == 'How many':
        ans = answer.answer_how_many(q, best)
    elif q_tokens[0] == 'Where':
        ans = answer.answer_where(q, best)
    elif q_tokens[0] == 'When':
        ans = answer.answer_when(q, best)
    else:
        ans = answer.answer_binary(q, best)
    answers.append(ans)

for ans in answers:
    sys.stdout.write(ans+'\n')
