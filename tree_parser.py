__author__ = 'laceyliu'
import stanford_utils
from nltk import Tree
parser = stanford_utils.new_parser()

def sents_to_trees(sentences):
    return parser.raw_parse_sents(sentences)

def sent_to_tree(sentence):
    t = parser.raw_parse(sentence)
    return Tree(t,list(t))

def tree_to_sent(tree):
    if tree == None:
        return ""
    return ' '.join(tree.leaves())

def get_phrases(tree, pattern, reversed, sort):
    phrases = []
    for t in tree.subtrees():
        if t.label() == pattern:
            phrases.append(t)
    if sort == True:
        phrases = sorted(phrases, key=lambda x:len(x.leaves()), reverse=reversed)
    return phrases

# # test = 'Perl was originally named "Pearl".'
# # test_tree = sent_to_tree(test)
# # # traverse(test_tree)
# # # test_sent = tree_to_sent(test_tree)
# # # print test_tree
# # # print test_sent
# #
# # test = "Clinton Drew, born on March 9, 1983, is an American soccer player who plays for Tottenham Hotspur and the United States national team."
# # tree = sent_to_tree(test)
# # vplist = get_phrases(tree, "VP")
# # pplist = get_phrases(tree, "PP")
# # nplist = get_phrases(tree, "NP")
#
# # for vp in vplist:
# #     print vp
# for np in nplist:
#     print np


def pre_process_sentence(input_sentence):
    simple_predicate_check = False
    apposition_check = False
    relative_clause_check = False
    good_sentences = []
    final_sentences = []

    #english_parser = StanfordParser("stanford-parser.jar", "stanford-parser-3.4.1-models.jar")
    english_parser = stanford_utils.new_parser()
    sentences = english_parser.raw_parse(input_sentence)

    #check if sentence is in the form S -> NP VP .
    for t in sentences:
        for tr in t:
            tr1 = str(tr)
            s1 = Tree.fromstring(tr1)
            s2 = s1.productions()

    #Turn sentences into NP VP format
    found_NP = False
    while found_NP == False:
        if s1[0].label() == '.' or s1[0].label() == ':':
            found_NP = True
        elif s1[0].label() != 'NP':
            #print s1[0].label()
            s1.pop(0)
        else:
            found_NP = True


    if s1.label() == 'S' and s1[0].label() == 'NP' and s1[1].label() == 'VP' and s1[2].label() == '.':
        simple_predicate_check = True
        #print "TRUE"

    #Split sentences into NP VP
    np_found = False
    np_start = ''
    vp_start = ''
    vp_repeated = False
    vp_re_counter = 0
    vp_re_list = []
    for i in s1.subtrees():
        #Process NP
        if (i.label() == 'NP' and len(i.leaves()) < 4 and np_found == False and simple_predicate_check == True):
            temp_list2 = i.leaves()
            for f in temp_list2:
                if np_start == '':
                    np_start = np_start + f
                elif np_start != '':
                    np_start = np_start + ' ' + f
            np_found = True

        #Proccess VP
        if (i.label() == 'VP' and vp_repeated == False and simple_predicate_check == True):
            temp_list = i.leaves()
            for y in xrange(min(len(vp_re_list), len(temp_list))):
                if len(vp_re_list) > 0 and (temp_list[y] in vp_re_list):
                    vp_re_counter += 1
            if (vp_re_counter < 3):
                for u in temp_list:
                    if(vp_start == ''):
                        vp_start = vp_start + u
                    elif(vp_start != ''):
                        vp_start = vp_start + ' ' + u
                vp_start = np_start + ' ' + vp_start
                good_sentences.append(vp_start)
                #print good_sentences
                vp_start = ''
                for h in xrange(len(temp_list)):
                    vp_re_list.append(temp_list[h])
            elif(vp_re_counter >= 3):
                vp_repeated = True
    return good_sentences

def get_final_sentences(input_sentence_list):
    output = []
    for i in input_sentence_list:
        temp_list = pre_process_sentence(i)
        for sentence in temp_list:
            if (sentence[-1] != '.'):
                sentence = sentence + '.'
            if (sentence[0].isupper() != True):
                sentence = ' '.join(word[0].upper() + word[1:] for word in sentence.split())
            print "Original:    "+i
            print "Processed:   "+sentence
            print
            output.append(sentence)
    return output

