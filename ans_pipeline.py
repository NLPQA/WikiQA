__author__ = 'laceyliu'

import sys
import doc_parser
from nltk import tokenize
import ans_ranker
import answer

# wiki_path, question_path = sys.argv[1], sys.argv[2]

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
        q_tokens = tokenize.word_tokenize(q)
        sys.stdout.write("Q: " + q + '\n')
        # for rs in ranked_sents:
        #     sys.stdout.write("A: " + rs[0] + '\n')

        ans = ""
        if q_tokens[0] == 'What':
            ans = answer.answer_what(q, ranked_sents[:min(6, len(ranked_sents))], title)
        elif q_tokens[0] == 'Who':
            ans = answer.answer_who(q, ranked_sents[:min(6, len(ranked_sents))], title)
        elif q_tokens[0] == 'Why':
            best = ans_ranker.rerank_why(ranked_sents[:6])
            ans = answer.answer_why(q, best)
        elif q_tokens[0] == 'How' and q_tokens[1] == 'many':
            ans = ""
            best = ans_ranker.rerank_num(ranked_sents[:6])
            if len(best) > 0:
                ans = answer.answer_how_many(q, best)
            else:
                best = ranked_sents[0][0]
        elif q_tokens[0] == 'Where':
            best = answer.answer_where(q, ranked_sents[:6], title)
        elif q_tokens[0] == 'When':
            best = answer.answer_when(q, ranked_sents[:min(6, len(ranked_sents))], title)
        elif q_tokens[0] == "Which":
            ans = answer.answer_which(q, best)

        elif q_tokens[0] == "How":
            ans = ""
        else:
            ans = answer.answer_binary(q, ranked_sents[:min(6, len(ranked_sents))], title)
        answers.append(ans)
        #print best
        print
        for sent in ranked_sents:
            print sent[0]

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

# wiki_path, question_path = "test/a6.htm", "test/a6q.txt"
# main(wiki_path, question_path)