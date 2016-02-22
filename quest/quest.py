__author__ = 'laceyliu'

import sys
import parser
import stanford_utils
import gold_standard_parser
# article, qnum = sys.argv[1], sys.argv[2]
article, qnum = gold_standard_parser.findPath("Slumdog_Millionaire"), 5
# article, qnum = 'test.txt', 5

sentences = parser.doc_to_sentence(article)
stanford_parser = stanford_utils.new_parser()
trees = stanford_parser.raw_parse_sents(sentences)
appositions = parser.find_appos(trees)
if len(appositions) > 0:
    appo_sents = parser.appo_to_sent(appositions)
    trees += parser.sents_to_trees()

preds = parser.find_preds(trees)

print preds