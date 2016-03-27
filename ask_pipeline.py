import math
import doc_parser
import nltk
import tree_parser
import ask
import stanford_utils
import ginger_python2 as grammar_checker


import sys
tagger = stanford_utils.new_NERtagger()
why_keywords = ["because", "therefore", "thus", "so that", "due to", "in order to"]
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
    return False

def contains_quant(sent, tagged_sent):
    tokens = nltk.tokenize.word_tokenize(sent)
    for i in xrange(0, len(tokens)):
        if str.isdigit(tokens[i]):
            if i + 1 < len(tokens) and tagged_sent[i+1][1].endswith('s'):
                return True
    return False


def main(wiki_path, n):
    title, sents = doc_parser.doc_to_sents(wiki_path)
    sents = [sent for sent in sents if 10 <= sent.count(" ") <= 30]
    sents = sents[:2*n]
    questions = []

    for sent in sents:
        parsed_sent = tree_parser.sent_to_tree(sent)
        pps = tree_parser.get_phrases(parsed_sent, "PP", reversed=False, sort=False)
        vps = tree_parser.get_phrases(parsed_sent, "VP", reversed=False, sort=False)
        nps = tree_parser.get_phrases(parsed_sent, "NP", reversed=False, sort=False)
        tagged_sent = tagger.tag(nltk.tokenize.word_tokenize(sent))

        # bonus for average len
        score = 20 - math.fabs(sent.count(" ")-10)
        # bonus for more pps
        score += len(pps)-1

        # bonus for question difficulties
        # distribute sents to generators
        # binary question
        binary_q = ask.get_binary(sent).capitalize()
        binary_q, errs = grammar_checker.correct_sent(binary_q)
        # deductions for errors
        questions.append((binary_q, score-errs+2))

        # why
        if contains_reason(tagged_sent):
            question = ask.get_why(sent).capitalize()
            # correct grammar and find errors
            question, errs = grammar_checker.correct_sent(question)
            # deductions for errors
            questions.append((question, score-errs+5))

        # how-many
        if contains_quant(sent, tagged_sent):
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
            question = ask.get_who(sent).capitalize()
            # correct grammar and find errors
            question, errs = grammar_checker.correct_sent(question)
            # deductions for errors
            questions.append((question, score-errs+4))
        else:
            question = ask.get_what(sent).capitalize()
            # correct grammar and find errors
            question, errs = grammar_checker.correct_sent(question)
            # deductions for errors
            questions.append((question, score-errs+3))

    ranked_questions = sorted(questions, key=lambda x:(-x[1],x[0]))[:n]

    for question in ranked_questions:
        sys.stdout.write(question[0]+"\n")

main("test/a6.htm", 30)
# main(sys.argv[1], int(sys.argv[2]))