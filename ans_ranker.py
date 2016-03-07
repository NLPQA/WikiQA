__author__ = 'laceyliu'

import doc_parser
import math
stopwords = doc_parser.stopwords


def get_tfidf(q_vect, s_vect, idfs):
    tfidf = 0.0
    for q_token, q_cnt in q_vect.items():
        if q_token in s_vect.keys():
            tfidf += s_vect[q_token]*idfs[q_token]
    return tfidf

def get_boolean(q_vect, s_vect):
    boolean = 0
    for q_token, q_cnt in q_vect.items():
        if q_token in s_vect.keys():
            boolean += 1
    return boolean

def get_cosine(q_vect, s_vect):
    cosine = 0.0
    for key in q_vect:
        if key in s_vect:
            cosine += q_vect[key]*s_vect[key]
    cosine /= (get_vect_size(q_vect)*get_vect_size(s_vect))
    return cosine

def get_vect_size(vect):
    size = 0.0
    for key, cnt in vect.items():
        size += cnt*cnt
    return math.sqrt(size)


def rank_sents(q_vect, sents, sent_vects, sent_idfs):
    rank = []
    filtered_sents = []
    for i in xrange(0, len(sent_vects)):
        if get_boolean(q_vect, sent_vects[i]) >= len(q_vect)-3:
            filtered_sents.append((sents[i], sent_vects[i]))
    for (sent, sent_v) in filtered_sents:
        rank.append((sent, get_tfidf(q_vect, sent_v, sent_idfs)))
        # rank.append((sent, get_cosine(q_vect, sent_v)))

        # rank.append((sents[i], get_boolean(q_vect, sent_vects[i], sent_idfs)))

    # for i in xrange(0, len(sent_vects)):
    #     # rank.append((sents[i], get_tfidf(q_vect, sent_vects[i], sent_idfs)))
    #     # rank.append((sents[i], get_boolean(q_vect, sent_vects[i], sent_idfs)))
    #     rank.append((sents[i], get_cosine(q_vect, sent_vects[i])))
    rank = sorted(rank, key=lambda x:(-x[1],x[0]))
    return rank[:5]

