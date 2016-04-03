__author__ = 'laceyliu'
# from nltk import tokenize
# from nltk import pos_tag
# s = "What is Delta Cancri also known as?"
# tagged = pos_tag(tokenize.word_tokenize(s))
# print tagged

import tree_parser
qs = [
    "What is the magnitude of the brightest star in Gemini?",
    "What is the maximum rate of Geminids meteor showers?",
    "What is the magnitude of M35 (NGC 2168)?",
    "What is the length of production cycle of Prisoner of Azkaban?"
]

qs2 = [
    "What was Perl originally named?",
    "What is Delta Cancri also known as?"
]

qs3 = [
    "What is the three-letter abbreviation for the constellation?",
    "What was the first club Beckham played for?"
       ]
for q in qs3:
    tree = tree_parser.sent_to_tree(q)
    for t in tree:
        print(t)