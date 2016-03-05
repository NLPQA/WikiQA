__author__ = 'laceyliu'

import sys
import doc_parser
import stanford_utils
import gold_standard_parser
# article, qnum = sys.argv[1], sys.argv[2]
article, qnum = gold_standard_parser.findPath("Slumdog_Millionaire"), 5
# article, qnum = 'test.txt', 5

sentences = doc_parser.doc_to_sents(article)

sentences = [ sent+"." for sent in sentences if sent.count(" ")<= 30 and sent.count(" ") >= 7]
if len(sentences) > 50:
    sentences = sentences[:50]

print sentences

#
#
# stanford_parser = stanford_utils.new_parser()
# trees = stanford_parser.raw_parse_sents(sentences)
# appositions = parser.find_appos(trees)
# if len(appositions) > 0:
#     appo_sents = parser.appo_to_sent(appositions)
#     trees += parser.sents_to_trees()
#
# preds = parser.find_preds(trees)
#
# print preds