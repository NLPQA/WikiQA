__author__ = 'laceyliu'

import doc_parser
import math
import stanford_utils
import nltk

stopwords = doc_parser.stopwords
tagger = stanford_utils.new_NERtagger()
def rerank_when(sents):
    for sent in sents:
        tagged_pp = tagger.tag(nltk.tokenize.word_tokenize(sent[0]))
        for tup in tagged_pp:
            if tup[1] == "DATE" or tup[1] == "TIME":
                return sent[0]
    return sents[0][0]

def rerank_where(sents):
    for sent in sents:
        tagged_pp = tagger.tag(nltk.tokenize.word_tokenize(sent[0]))
        for tup in tagged_pp:
            if tup[1] == "LOCATION" or tup[1] == "ORGANIZATION":
                return sent[0]
    return sents[0][0]

def rerank_why(sents):
    keywords = ["because", "therefore", "so", "in order to", "since", "as", "due to"]
    for sent in sents:
        for keyword in keywords:
            if keyword in sent[0]:
                return sent[0]
    return sents[0][0]

def rerank_num(sents, keyword):
    for sent in sents:
        num = filter(str.isdigit, sent[0])
        if len(num) > 0 and keyword in sent[0]:
            return sent[0]
    return ""

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
    cosine /= ((get_vect_size(q_vect)+1)*(get_vect_size(s_vect)+1))
    return cosine

def get_vect_size(vect):
    size = 0.0
    for key, cnt in vect.items():
        size += cnt*cnt
    return math.sqrt(size)


def rank_sents(q_vect, sents, sent_vects, sent_idfs):
    # rank = []
    rank_cos = []
    rank_tfidf = []
    filtered_sents = []
    for i in xrange(0, len(sent_vects)):
        if get_boolean(q_vect, sent_vects[i]) >= len(q_vect)-3:
            filtered_sents.append((sents[i], sent_vects[i]))
    for (sent, sent_v) in filtered_sents:
        tfidf = get_tfidf(q_vect, sent_v, sent_idfs)
        cosine =  get_cosine(q_vect, sent_v)
        rank_cos.append((sent, cosine))
        rank_tfidf.append((sent,tfidf))

        # rank.append((sents[i], get_boolean(q_vect, sent_vects[i], sent_idfs)))

    # for i in xrange(0, len(sent_vects)):
    #     # rank.append((sents[i], get_tfidf(q_vect, sent_vects[i], sent_idfs)))
    #     # rank.append((sents[i], get_boolean(q_vect, sent_vects[i], sent_idfs)))
    #     rank.append((sents[i], get_cosine(q_vect, sent_vects[i])))
    # rank = sorted(rank, key=lambda x:(-x[1],x[0]))
    rank_cos = sorted(rank_cos, key=lambda x:(-x[1],x[0]))[:5]
    rank_tfidf = sorted(rank_tfidf, key=lambda x:(-x[1],x[0]))[:5]
    rank = []
    i_cos, i_tf, i = 0, 0, 0
    size = min(len(rank_cos), len(rank_tfidf))
    while (i < size):
        if rank_cos[i_cos][0] != rank_tfidf[i_tf][0]:
            if len(rank_cos[i_cos][0]) < len(rank_tfidf[i_tf][0]):
                rank.append(rank_cos[i_cos])
                i_cos+=1
                i+=1
            else:
                rank.append(rank_tfidf[i_tf])
                i_tf+=1
                i+=1
        else:
            rank.append(rank_cos[i_cos])
            i_cos+=1
            i_tf+=1
            i+=1
    return rank[:size]

def rerank_match(q_vect, sents, stop_words):
    mis_matched_num = []
    for sent in sents:
        s_vect = doc_parser.sent_to_vect(sent[0].lower())
        mis_matched = 0
        for token, cnt in q_vect.items():
            if token not in s_vect and (token not in stop_words):
                mis_matched += cnt
        mis_matched_num += [mis_matched]
    print q_vect, mis_matched_num
    best_idx = mis_matched_num.index(min(mis_matched_num))
    return sents[best_idx][0]