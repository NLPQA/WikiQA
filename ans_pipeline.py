__author__ = 'laceyliu'

import sys
import doc_parser
from nltk import tokenize
import ans_ranker
import answer

# wiki_path, question_path = sys.argv[1], sys.argv[2]

def quest_to_state(q):
   tokens = q.split(" ")
   if tokens[0].startswith("Wh"):
       return ' '.join(tokens[2:])
   if tokens[0] == "How" and tokens[1] == "many":
       return ' '.join(tokens[3:])
   return ' '. join(tokens[1:])

# wiki_path, question_path = "test_wiki.htm", "test_quests.txt"
wiki_path, question_path = "test/a5.htm", "test/a5q.txt"

sents = doc_parser.doc_to_sents(wiki_path)
sent_vects = doc_parser.doc_to_vects(wiki_path)
sent_idfs = doc_parser.doc_to_idfs(wiki_path)
quests = []

with  open(question_path) as f:
    quests = f.read().splitlines()
answers = []
for q in quests:
    q2 = quest_to_state(q)
    q_vect = doc_parser.sent_to_vect(q2)
    ranked_sents = ans_ranker.rank_sents(q_vect, sents, sent_vects, sent_idfs)
    best = ranked_sents[0][0]
    q_tokens = tokenize.word_tokenize(q)
    sys.stdout.write("Q: " + q + '\n')
    # for rs in ranked_sents:
    #     sys.stdout.write("A: " + rs[0] + '\n')

    ans = ""
    if q_tokens[0] == 'What':
        ans = answer.answer_what(q, best)
    elif q_tokens[0] == 'Who':
        ans = answer.answer_who(q, best)
    elif q_tokens[0] == 'Why':
        ans = answer.answer_why(q, best)
    elif q_tokens[0] == 'How' and q_tokens[1] == 'many':
        ans = ""
        # for sent in ranked_sents:
        #     num = filter(str.isdigit, sent[0])
        #     if len(num) > 0:
        #         ans = answer.answer_how_many(q, sent[0])
        #         break
        for s in ranked_sents[:5]:
            print s[0]
    elif q_tokens[0] == 'Where':
        ans = answer.answer_where(q, best)
    elif q_tokens[0] == 'When':
        ans = answer.answer_when(q, best)
        #ans = answer.ans_when(q2, ranked_sents)
    elif q_tokens[0] == "Which":
        ans = answer.answer_which(q, best)
    else:
        ans = answer.answer_binary(q, best)
    answers.append(ans)
    sys.stdout.write("A: " + (ans if len(ans)>0 else best) + '\n')
    sys.stdout.write("----------\n")


# for quest, ans in zip(quests, answers):
#     sys.stdout.write("Q: " + quest + '\n')
#     sys.stdout.write("A: " + ans + '\n')
#     sys.stdout.write("----------\n")

