__author__ = 'laceyliu'
import nltk
from nltk.tree import Tree

import stanford_utils
# select sentences
# - discard long sentences (>30 words)
# - discard short sentences (< 7 words)
def doc_to_sentence(article):
    with open(article, 'r') as f:
        content = f.read().decode('utf-8').encode('ascii', 'ignore').replace('\n', '').replace('?', '.').replace('!', '.')
        sentences = content.split('.')
    f.close()

    sentences2 = [s for s in sentences if s.count(' ') < 20 and s.count(' ') > 7]
    if len(sentences2) > 100:
        sentences = sentences[:100]
    return sentences2

def sents_to_trees(sentences):
    parser = stanford_utils.new_parser()

    return parser.raw_parse_sents(sentences)

APPO_PATTERN = ('S', (('NP', ('NP', ',', 'NP', ',')), 'VP', '.'))
PREDICATE_PATTERN = ('ROOT', (('S', ('NP', 'VP', '.')),))

def is_match(tree, pattern):
  for node in tree:
      # base case: pattern is single tag
      if not isinstance(pattern, tuple):
        return node.label() == pattern
      # recursive case
      else:
        parent = pattern[0]
        children = pattern[1]
        if node.label() == parent and len(node) == len(children): # parent matches
          for i in xrange(len(node)): # check that all children match
            ith_child = node[i]
            if not is_match(ith_child, children[i]):
              return False
          return True

def search_for_matches(parse_tree, pattern):
  matches = []
  if is_match(parse_tree, pattern):
    matches.append(parse_tree)
  for child in parse_tree:
    if isinstance(child, Tree):
      matches += search_for_matches(child, pattern)
  return matches

def find_appos(parse_trees):
  appos = []
  for parse_tree in parse_trees:
    # look for appositions; add just the NP tuples to pattern_matches
    appos += [(s[0,0], s[0,2]) for
        s in search_for_matches(parse_tree, APPO_PATTERN)]
  return appos

def find_preds(parse_trees):
  preds = []
  for parse_tree in parse_trees:
    if is_match(parse_tree, PREDICATE_PATTERN):
      preds.append(parse_tree[0])
  return preds


def tree_to_sent(tree):
    return ' '.join(tree.leaves())

def appo_to_sent(appo):
    np1, np2 = appo[0], appo[1]
    head = find_noun(np1)
    be = 'are' if head.label().endWith('S') else 'is'
    return ' '.join([tree_to_sent(np1), be, tree_to_sent(np2)])+'.'

def find_noun(np):
    n = np
    while n.label() == 'NP':
        found = False
        for c in n:
            if c.label().startWith('N'):
                n = c
                found = True
                break
        if not found:
            return None
    return n

