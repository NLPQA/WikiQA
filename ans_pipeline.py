__author__ = 'laceyliu'

import sys
import doc_parser
from nltk import tokenize
import ans_ranker
import answer

# wiki_path, question_path = sys.argv[1], sys.argv[2]
mds = ["did", "do", "does", "di", "do", "doe"]
def quest_to_state(q):
   q = q.replace("?", ".")
   tokens = q.split(" ")
   if tokens[0].startswith("Wh"):
       return ' '.join(tokens[2:])
   if tokens[0] == "How" and tokens[1] == "many":
       return ' '.join(tokens[3:])
   return ' '. join(tokens[1:])

wiki_path, question_path = "a6.htm", "a6.txt"

def main(wiki, qpath):
    title, sents = doc_parser.doc_to_sents(wiki_path)
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
        title_tokens = title.lower().split(" ")
        reranked_best, miss = ans_ranker.rerank_match(q_vect, ranked_sents[:6], mds+title_tokens)
        q_tokens = tokenize.word_tokenize(q)
        # if "Who" in q:
        #     sys.stdout.write("Q: " + q.capitalize()  + '\n')
        sys.stdout.write("Q: " + (q.capitalize() +'\n'))
        # for sent in ranked_sents[:6]:
        #        print sent[0]
        if q_tokens[0] == 'What' or 'what' in q_tokens:
            ans = answer.answer_what(q, reranked_best)
            best = reranked_best
        elif q_tokens[0] == 'Who' or 'who' in q_tokens:
            ans = answer.answer_who(q, reranked_best)
            best = reranked_best
        elif q_tokens[0] == 'Why' or 'why' in q_tokens:
            best = ans_ranker.rerank_why(ranked_sents[:6])
            ans = answer.answer_why(q, best)
        elif q_tokens[0] == 'How' and q_tokens[1] == 'many':
            ans = ""
            best = ans_ranker.rerank_num(ranked_sents[:6], q_tokens[2])
            if len(best) > 0:
                ans = answer.answer_how_many(q, best)
            else:
                best = ranked_sents[0][0]
        elif q_tokens[0] == 'Where' or 'where' in q_tokens:
            ans = answer.answer_where(reranked_best)
            best = reranked_best
        elif q_tokens[0] == 'When' or 'when' in q_tokens:
            ans = answer.answer_when(reranked_best)
            best = reranked_best
        elif q_tokens[0] == "Which" or 'which' in q_tokens:
            ans = answer.answer_which(q, best)
        elif q_tokens[0] == "How" or 'how' in q_tokens:
            ans = ""
        else:
            ans = answer.answer_binary(reranked_best, miss)
            best = reranked_best
        answers.append(ans.capitalize() if ans != None and len(ans)>0 else best)
        print best
        # print
        # for sent in ranked_sents:
        #     print sent[0]

        # if "Who" in q:
        #     sys.stdout.write("S: " + best + '\n')
        #     sys.stdout.write("A: " + (ans.capitalize() if ans != None and len(ans)>0 else best) + '\n')
        #     sys.stdout.write("----------\n")

        sys.stdout.write("A: " + (ans.capitalize() if len(ans)>0 else best) + '\n')
        sys.stdout.write("----------\n")



for i in xrange(1, 9):
    if i == 4:
        continue
    print i

    wiki_path, question_path = "test/a"+str(i)+".htm", "test/a"+str(i)+"q.txt"
    main(wiki_path, question_path)
# for quest, ans in zip(quests, answers):
#     sys.stdout.write("Q: " + quest + '\n')
#     sys.stdout.write("A: " + ans + '\n')
#     sys.stdout.write("----------\n")
