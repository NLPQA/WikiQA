__author__ = 'laceyliu'

import nltk
import nltk.tokenize
import nltk.tag
import nltk.stem
import stanford_utils
from random import randint
from nltk.corpus import wordnet as wn

def stem(word):
    return wn.morphy(word).encode('ascii', 'ignore')

def get_binary(sentence, twist):
    question = ""
    sent = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(sent)
    if randint(0,9) < 4 and twist:
        tagged = twist_statement(tagged)
    for i in xrange(len(tagged)):
        if tagged[i][1] == 'MD' or tagged[i][0] == 'have' or (tagged[i][0] == 'has' and tagged[i][1] == 'VBZ') or tagged[i][0] == 'am'  or tagged[i][0] == 'are' or tagged[i][0] == 'was' or(tagged[i][0] == 'is' and tagged[i][1] == 'VBZ'):
            if tagged[0][1] != 'NNP' or tagged[0][1] != 'NNPS':
                tagged[0] = (tagged[0][0], tagged[0][1])
            tagged.insert(0, tagged.pop(i))
            break
        elif tagged[i][1] == 'VBD':
            tagged[i] = (stem(tagged[i][0]), 'VB')
            if tagged[0][1] != 'NNP' or tagged[0][1] != 'NNPS':
                tagged[0] = (tagged[0][0], tagged[0][1])
            tagged.insert(0, ('did', 'MD'))
            break
        elif tagged[i][1] == 'VBZ':
            tagged[i] = (stem(tagged[i][0]), 'VB')
            if tagged[0][1] != 'NNP' or tagged[0][1] != 'NNPS':
                tagged[0] = (tagged[0][0], tagged[0][1])
            tagged.insert(0, ('Does', 'MD'))
            break
        elif tagged[i][1] == 'VBP':
            tagged[i] = (stem(tagged[i][0]), 'VB')
            if tagged[0][1] != 'NNP' or tagged[0][1] != 'NNPS':
                tagged[0] = (tagged[0][0], tagged[0][1])
            tagged.insert(0, ('Do', 'MD'))
            break

    for j in xrange(len(tagged)):
        if j < len(tagged) - 2:
            question += tagged[j][0] + ' '
        elif j >= len(tagged) - 2 and tagged[j][0] != '.':
            question += tagged[j][0]
        elif twist:
            question += '?'
    return question

def twist_statement(tagged_sent):
    twisted = []
    for tagged_token in tagged_sent:
        # if tagged_token[1] == 'JJ' and ('-' not in tagged_token[0]):
        #     synsets = wn.synset(tagged_token[0]+".a.01").lemmas()
        #     con = [word.name() for word in synsets]+[word.name() for word in synsets[0].antonyms()]
        #     rd = randint(0,len(con)-1)
        #     if randint(0,9) < 4:
        #         twisted.append(tagged_token)
        #     else:
        #         twisted.append((con[rd],tagged_token[1]))
        if str.isdigit(tagged_token[0]):

        #elif str.isdigit(tagged_token[0]):
            num = int(tagged_token[0])+randint(0,9)
            if randint(0,9) < 4:
                twisted.append(tagged_token)
            else:
                twisted.append((str(num),tagged_token[1]))
        else:
            twisted.append(tagged_token)
    return twisted
# sent = 'Tom is a talented student at CMU, which is rich since 1990. '
# # tokenized_sent = nltk.word_tokenize(sent)
# # tagged = nltk.pos_tag(tokenized_sent)
# for i in xrange(0, 5):
#     print get_binary(sent)

def get_who(sentence):
    # tokenize into words for each sentence
    sent = nltk.word_tokenize(sentence)
    # tag for words in each sentence
    tagged = nltk.pos_tag(sent)
    question = ""
    for i in range(0,len(tagged)):
        question = ''
        start = 0
        if (tagged[i][1] == 'MD' or tagged[i][1] == 'VBD' or tagged[i][1] == 'VBZ' or tagged[i][0] == 'has' or tagged[i][1] == 'is' or tagged[i][1] == 'was'or tagged[i][1] == 'are'):
            if tagged[i][1] == 'MD':
                start = 1
                question += 'Who '
            elif tagged[i][0] == 'has':
                if tagged[i+1][1][0:1] == 'V':
                    question += 'Who has '
                    start = i + 1
                else:
                    question += 'Who does have '
                    start = i + 1
            elif tagged[i][0] == 'is':
                question += 'Who is '
                start = i + 1
            elif tagged[i][0] == 'was':
                question += 'Who was '
                start = i + 1
            elif tagged[i][0] == 'are':
                question += 'Who are '
                start = i + 1
            elif tagged[i][1] == 'VBD':
                verb = tagged[i][0]
                question += 'Who ' + verb + ' '
                start = i + 1
            elif tagged[i][1] == 'VBZ':
                verb = tagged[i][0]
                question += 'Who ' + verb + ' '
                start = i + 1
            for j in range(start,len(tagged)):
                if j < len(tagged) - 2:
                    question += tagged[j][0] + ' '
                elif j >= len(tagged) - 2 and tagged[j][0] != '.':
                    question += tagged[j][0]
                else:
                    question += '?'
            break
    return question

def get_what(sentence):
    # tokenize into words for each sentence
    sent = nltk.word_tokenize(sentence)
    # tag for words in each sentence
    tagged = nltk.pos_tag(sent)
    question = ""
    for i in range(0,len(tagged)):
        question = ''
        start = 0
        if (tagged[i][1] == 'MD' or tagged[i][1] == 'VBD' or tagged[i][1] == 'VBZ' or tagged[i][0] == 'has' or tagged[i][1] == 'is' or tagged[i][1] == 'was'or tagged[i][1] == 'are'):
            if tagged[i][1] == 'MD':
                start = 1
                question += 'What '
            elif tagged[i][0] == 'has':
                if tagged[i+1][1][0:1] == 'V':
                    question += 'What has '
                    start = i + 1
                else:
                    question += 'What does have '
                    start = i + 1
            elif tagged[i][0] == 'is':
                question += 'What is '
                start = i + 1
            elif tagged[i][0] == 'was':
                question += 'What was '
                start = i + 1
            elif tagged[i][0] == 'are':
                question += 'What are '
                start = i + 1
            elif tagged[i][1] == 'VBD':
                verb = tagged[i][0]
                question += 'What ' + verb + ' '
                start = i + 1
            elif tagged[i][1] == 'VBZ':
                verb = tagged[i][0]
                question += 'What ' + verb + ' '
                start = i + 1
            for j in range(start,len(tagged)):
                if j < len(tagged) - 2:
                    question += tagged[j][0] + ' '
                elif j >= len(tagged) - 2 and tagged[j][0] != '.':
                    question += tagged[j][0]
                else:
                    question += '?'
            break
    return question
# test = 'I can attest that my own expenditure when going to Starbucks has increased, in lieu of these food products.'
# print get_what(test)
# test_2 = "Beckham played in central midfield in United's win over Bayern Munich in the 1999 UEFA Champions League Final"
# print get_what(test_2)

# def get_what(sentence):
#     words = nltk.word_tokenize(sentence)
#     tagged = nltk.pos_tag(words)
#     NN = []
#     start = 0
#     for i in range(0, len(tagged)):
#         if tagged[i][0] == 'is' or tagged[i][0] == 'are' or tagged[i][0] == 'was':
#             start = i
#             break;
#         if tagged[i][1][0:2] == 'NN':
#             NN.append(tagged[i][0])
#     question = 'What '
#     for j in range(start, len(tagged)):
#         if j < len(tagged) - 2:
#             question += tagged[j][0] + ' '
#         elif j >= len(tagged) - 2 and tagged[j][0] != '.':
#             question += tagged[j][0]
#         else:
#             question += '?'
#     return question

def concat(l):
    return reduce(lambda a, b: a+" "+b, l)

def get_howmany(sentence):
    d = nltk.tokenize.word_tokenize(sentence)
    tagged = nltk.tag.pos_tag(d)

    for i in xrange(len(tagged)):
        # Case: .(consequence).. because (reason).....
        if tagged[i][1] == "CD":
            for j in xrange(len(tagged[i:])):
                if tagged[i+j][1] == "NNS" or tagged[i+j][1] == "NN":
                    object = tagged[i+1:i+j+1]
                    main_sentence = d[:i]
                    main_sentence[0] = main_sentence[0].lower()
                    break
    question = "How many " + concat(map(lambda x: x[0], object)) + " " + concat(main_sentence)+"?"
    return question

def get_why(sentence):
    d = nltk.tokenize.word_tokenize(sentence)
    tagged = nltk.tag.pos_tag(d)
    consequence = ""
    for i in xrange(len(tagged)):
        # Case: .(consequence).. because (reason).....
        if tagged[i][0].lower() in ["since", "because"] and ("," not in d[i:]):
            consequence = reduce(lambda a, b: a+" "+b, d[:i-1])
            break
        # Case: because ..(reason).. , .(consequence)
        elif tagged[i][0].lower() in ["since", "because"] and ("," in d[i:]):
            consequence = reduce(lambda a, b: a+" "+b, d[d.index(",")+1:])
            break
        # other cases: due to ...
    question = get_binary(consequence, twist=False)
    question = "Why "+question+"?"
    return question



def get_where(sentence):

    binary_q = get_binary(sentence, twist=False)

    words = nltk.word_tokenize(binary_q)
    tagger = stanford_utils.new_NERtagger()
    ners = tagger.tag(words)
    tagged = nltk.pos_tag(words)

    for i in range(0, len(ners)):
        if tagged[i][0] == 'where':
            j = i+1
            while j < len(ners) and (ners[j][0] != ',' or ners[j][0] != '?'):
                j+=1
            if j > i+1:
                for k in xrange(0, j-i):
                    ners.pop(i)
                break

        if tagged[i][1] == 'IN':
            j = i+1
            while j < len(ners) and (ners[j][1] == 'ORGANIZATION' or ners[j][1] == 'LOCATION'):
                j+=1
            if j > i+1:
                for k in xrange(0, j-i):
                    ners.pop(i)
                break

    question = "Where " + ' '.join([w for (w, t) in ners])
    return question.strip()+"?"

def get_when(sentence):
    binary_q = get_binary(sentence, twist=False)
    words = nltk.word_tokenize(binary_q)
    tagger = stanford_utils.new_NERtagger()
    ners = tagger.tag(words)
    tagged = nltk.pos_tag(words)

    for i in range(0, len(ners)):
        if tagged[i][0] == 'during':
            j = i+1
            while j < len(ners) and (ners[j][0] == '~' or ners[j][0] == '-' or ners[j][0] != ',' or ners[j][0] != '?'):
                j+=1
            if j > i+1:
                for k in xrange(0, j-i):
                    ners.pop(i)
                break

        if tagged[i][0] == 'since' or tagged[i][0] == 'when' or tagged[i][0] == 'before' or tagged[i][0] == 'after':
            j = i+1
            while j < len(ners) and (ners[j][0] != ',' or ners[j][0] != '?'):
                j+=1
            if j > i+1:
                for k in xrange(0, j-i):
                    ners.pop(i)
                break
        if tagged[i][1] == 'IN':
            j = i+1
            while j < len(ners) and (ners[j][1] == 'DATE' or ners[j][1] == 'TIME'):
                j+=1

            if j > i+1:
                for k in xrange(0, j-i):
                    ners.pop(i)
                break
        if ners[i][1] == 'DATE' or ners[i][1] == 'TIME':
            j = i+1
            while j < len(ners) and (ners[j][1] == 'DATE' or ners[j][1] == 'TIME'):
                j+=1

            if j > i+1:
                for k in xrange(0, j-i):
                    ners.pop(i)
                break
    question = "When " + ' '.join([w for (w, t) in ners])+"?"
    return question

tests = ['Clinton Drew, born March 9, 1983, is an American soccer player who plays for Tottenham Hotspur and the United States national team.',
             'Growing up in Nacogdoches, Texas, Dempsey played for one of the top youth soccer clubs in the state, the Dallas Texans, before playing for Furman University\'s men\'s soccer team. ',
             'In 2004, Dempsey was drafted by Major League Soccer club New England Revolution, where he quickly integrated himself into the starting lineup. ',
             'Hindered initially by a jaw injury, he would eventually score 25 goals in 71 appearances with the Revolution.',
             'Between 2007 and 2012, Dempsey played for Premier League team Fulham and is the club\'s highest Premier League goalscorer of all time.',
             'Dempsey first represented the United States at the 2003 FIFA World Youth Championship in the United Arab Emirates. He made his first appearance with the senior team on November 17, 2004, against Jamaica; he was then named to the squad for the 2006 World Cup and scored the team\'s only goal of the tournament. ',
             'In the 2010 FIFA World Cup, Dempsey scored against England, becoming the second American, after Brian McBride, to score goals in multiple World Cup tournaments.']

# for test in tests:
#     print "========================\n"
#     print test
#     print get_binary(test)
    # print get_what(test)
    # print get_who(test)
    # print get_howmany(test)
    # print get_when(test)
    # print get_where(test)
    # print get_why(test)
