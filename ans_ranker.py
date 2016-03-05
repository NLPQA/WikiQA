__author__ = 'laceyliu'

import doc_parser


def get_tfidf(q_vect, s_vect, idfs):
    tfidf = 0.0
    for q_token, q_cnt in q_vect.items():
        if q_token in s_vect.keys():
            tfidf += s_vect[q_token]*idfs[q_token]
    return tfidf

def rank_sents(q_vect, sents, sent_vects, sent_idfs):
    rank = []
    for i in xrange(0, len(sent_vects)):
        rank.append((sents[i], get_tfidf(q_vect, sent_vects[i], sent_idfs)))
    rank = sorted(rank, key=lambda x:(-x[1],x[0]))
    return rank

