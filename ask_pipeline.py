import math
import doc_parser
import nltk
import tree_parser
import ask
import stanford_utils
import ginger_python2 as grammar_checker


import sys
tagger = stanford_utils.new_NERtagger()
why_keywords = ["because"]
def contains_reason(sent):
    for why_keyword in why_keywords:
            if why_keyword in sent:
                return True
    return False

def contains_time(tagged_sent):
    for tup in tagged_sent:
        if tup[1] == "DATE" or tup[1] == "TIME":
            return True
    return False

def contains_loc(tagged_sent):
    for tup in tagged_sent:
        if tup[1] == "LOCATION" or tup[1] == "ORGANIZATION":
            return True
    return False

def contains_name(tagged_sent):
    for tup in tagged_sent:
        if tup[1] == "PERSON":
            return True
        elif tup[0].lower() == "he" or tup[0].lower() == "she":
            return True
    return False

def contains_quant(sent, tagged_sent):
    tokens = nltk.tokenize.word_tokenize(sent)
    for i in xrange(0, len(tokens)):
        if str.isdigit(str(tokens[i])):
            if i + 1 < len(tokens) and tagged_sent[i+1][1].endswith('s'):
                return True
    return False

def preprocess_sents(sents):
    preds = []
    for sent in sents:
        tree = tree_parser.sent_to_tree(sent)
    if tree_parser.contains_appos(tree):
        preds += tree_parser.appps_to_sents(tree)
    else:
        pred = tree_parser.sent_to_predicate(tree)
        preds.append(pred)
    return preds

def main(wiki_path, n):
    title, sents = doc_parser.doc_to_sents(wiki_path)
    questions = []

    sents = [sent for sent in sents if 10 <= sent.count(" ") <= 30]
    sents = sents[:3*n]
    # preds = []
    # for sent in sents:
    #     tree = tree_parser.sent_to_tree(sent)
    #     if tree_parser.contains_appos(tree):
    #         preds += tree_parser.appps_to_sents(tree)
    #     else:
    #         pred = tree_parser.sent_to_predicate(tree)
    #         if 10 <= pred.count(" ") <= 30:
    #             preds.append(pred)
    #         if len(preds) > 2*n:
    #             break
    # for pred in preds:
    #     print pred
    for sent in sents:
        parsed_sent = tree_parser.sent_to_tree(sent)
        pps = tree_parser.get_phrases(parsed_sent, "PP", False, False)

        tagged_sent = tagger.tag(nltk.tokenize.word_tokenize(sent))

        # bonus for average len
        score = (20 - math.fabs(sent.count(" ")-10))*0.5
        # bonus for more pps
        score += len(pps)-1

        # bonus for question difficulties
        # distribute sents to generators
        # why
        if contains_reason(tagged_sent):
            question = ask.get_why(sent).capitalize()
            # correct grammar and find errors
            question, errs = grammar_checker.correct_sent(question)
            # deductions for errors
            questions.append((question, score-errs+5))

        # how-many
        elif contains_quant(sent, tagged_sent):
            question = ask.get_howmany(sent).capitalize()
            # correct grammar and find errors
            question, errs = grammar_checker.correct_sent(question)
            # deductions for errors
            questions.append((question, score-errs+5))

        # when
        if contains_time(tagged_sent):
            question = ask.get_when(sent).capitalize()
            # correct grammar and find errors
            question, errs = grammar_checker.correct_sent(question)
            # deductions for errors
            if (len(question) > 29):
                questions.append((question, score-errs+4))
        # where
        if contains_loc(tagged_sent):
            question = ask.get_where(sent).capitalize()
            # correct grammar and find errors
            question, errs = grammar_checker.correct_sent(question)
            # deductions for errors
            questions.append((question, score-errs+4))

        # who/what
        if contains_name(tagged_sent):
            question = ask.get_who(parsed_sent).capitalize()
            # correct grammar and find errors
            question, errs = grammar_checker.correct_sent(question)
            # deductions for errors
            questions.append((question, score-errs+3))
        else:
            question = ask.get_what(parsed_sent).capitalize()
            # correct grammar and find errors
            question, errs = grammar_checker.correct_sent(question)
            # deductions for errors
            questions.append((question, score-errs+2))

        # binary question
        binary_q = ask.get_binary(sent, twist=False).capitalize()
        binary_q, errs = grammar_checker.correct_sent(binary_q)
        # deductions for errors
        questions.append((binary_q, score-errs+2))

    ranked_questions = sorted(questions, key=lambda x:(-x[1],x[0]))
    ranked_questions = [q for q in ranked_questions if len(q[0]) > 0][:n]
    for question in ranked_questions:
        sys.stdout.write(question[0]+" "+"\n")

# import time
# for i in xrange(1, 9):
#     start = time.time()
#     if i == 4:
#         continue
#     print i
#     wiki_path = "test/a"+str(i)+".htm"
#     main(wiki_path, i)
#     print time.time() - start
main("test/a6.htm", 10)
# main(sys.argv[1], int(sys.argv[2]))
