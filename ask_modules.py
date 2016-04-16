__author__ = 'laceyliu'

import re
from random import randint
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn

def stem(word):
    stemmed = wn.morphy(word).encode('ascii', 'ignore')
    return stemmed if len(stemmed) > 0 else word

# get basic form for verb (set pos = 'v' for verb)
def basicForm(word, pos):
    exceptions = wn._exception_map[pos]
    if word in exceptions:
        return exceptions[word][0]
    else:
        return WordNetLemmatizer().lemmatize(word, pos)

def get_binary(sentence, tagged, ners, twist):
    question = ""
    bes = ["am", "are", "was", "were", "have", "has", "is"]
    # sent = nltk.word_tokenize(sentence)
    # tagged = nltk.pos_tag(sent)
    if randint(0,9) < 4 and twist:
        tagged = twist_statement(tagged)

    if len(tagged) == 0:
        return ""
    # lower the first letter if it is not NNP or NNPS
    if tagged[0][1] != 'NNP' and tagged[0][1] != 'NNPS':
            #if ners[0][1] != 'PERSON' and ners[0][1] != 'ORGANIZATION' and ners != 'LOCATION':
        tagged[0] = (tagged[0][0].lower(), tagged[0][1])
        ners[0] = (ners[0][0].lower(), ners[0][1])

    i = 0
    while i < len(tagged):
        if tagged[i][0] in bes:
            ners.insert(0, ners.pop(i))
            tagged.insert(0, tagged.pop(i))
            break
        elif tagged[i][1] == 'MD':
            ners.insert(0, ners.pop(i))
            tagged.insert(0, tagged.pop(i))
            break
        elif tagged[i][1] == 'VBD':
            ners[i] = (stem(tagged[i][0]), 'O')
            tagged[i] = (stem(tagged[i][0]), 'VBP')
            ners.insert(0, ('did','O'))
            tagged.insert(0, ('did','MD'))
            break
        elif tagged[i][1] == 'VBZ':
            ners[i] = (stem(tagged[i][0]), 'O')
            tagged[i] = (stem(tagged[i][0]), 'VBP')
            ners.insert(0, ('does','O'))
            tagged.insert(0, ('does','MD'))
            break
        elif tagged[i][1] == 'VBP':
            ners[i] = (stem(tagged[i][0]), 'O')
            tagged[i] = (stem(tagged[i][0]), 'VBP')
            ners.insert(0, ('do','O'))
            tagged.insert(0, ('do','MD'))
            break
        i+=1

    for i in xrange(len(tagged)-1):
        question += ' ' + tagged[i][0]

    return question.strip(), tagged, ners

def twist_statement(tagged_sent):
    twisted = []
    for tagged_token in tagged_sent:
        if tagged_token[1] == 'JJ' and ('-' not in tagged_token[0]):
            synsets = wn.synset(tagged_token[0]+".a.01").lemmas()
            con = [word.name() for word in synsets]+[word.name() for word in synsets[0].antonyms()]
            rd = randint(0,len(con)-1)
            if randint(0,9) < 4:
                twisted.append(tagged_token)
            else:
                twisted.append((con[rd],tagged_token[1]))

        elif str.isdigit(tagged_token[0]):
            num = int(tagged_token[0])+randint(0,9)
            if randint(0,9) < 4:
                twisted.append(tagged_token)
            else:
                twisted.append((str(num),tagged_token[1]))
        else:
            twisted.append(tagged_token)
    return twisted

# # generate who question
# def get_who(tree):
#     question = "who "
#     verbP = re.compile("^V[BP].{0,1}$")
#     for node in tree[0]:
#         if node.label() != "NP":
#             if node.label() == "VP":
#                 for i in xrange(len(node)):
#                     if node[i].label() == "MD":
#                         break;
#                     elif node[i].label() == "VBZ":
#                         if node[i][0] != "is" and not (node[i][0] == "has" and i+1<len(node) and verbP.match(node[i+1].label())):
#                             question = "who does" + question[question.find(" "):]
#                             for j in xrange(i, len(node)):
#                                 if node[j].label() == "VBZ":
#                                     node[j][0] = basicForm(node[j][0], 'v')
#                             break;
#                     elif node[i].label() == "VBD":
#                         if node[i][0] != "was" and node[i][0] != "were" and not (node[i][0] == "had" and i+1<len(node) and verbP.match(node[i+1].label())):
#                             question = "who did" + question[question.find(" "):]
#                             for j in xrange(i, len(node)):
#                                 if node[j].label() == "VBD":
#                                     node[j][0] = basicForm(node[j][0], 'v')
#             question += " ".join([leave for leave in node.leaves()]) + " "
#     question = question[:len(question)-3] + "?"
#     return question
#
# # generate what question
# def get_what(tree):
#     question = "what "
#     verbP = re.compile("^V[BP].{0,1}$")
#     for node in tree[0]:
#         if node.label() != "NP":
#             if node.label() == "VP":
#                 for i in xrange(len(node)):
#                     if node[i].label() == "MD":
#                         break;
#                     elif node[i].label() == "VBZ":
#                         if node[i][0] != "is" and not (node[i][0] == "has" and i+1<len(node) and verbP.match(node[i+1].label())):
#                             question = "what does" + question[question.find(" "):]
#                             for j in xrange(i, len(node)):
#                                 if node[j].label() == "VBZ":
#                                     node[j][0] = basicForm(node[j][0], 'v')
#                             break;
#                     elif node[i].label() == "VBD":
#                         if node[i][0] != "was" and node[i][0] != "were" and not (node[i][0] == "had" and i+1<len(node) and verbP.match(node[i+1].label())):
#                             question = "what did" + question[question.find(" "):]
#                             for j in xrange(i, len(node)):
#                                 if node[j].label() == "VBD":
#                                     node[j][0] = basicForm(node[j][0], 'v')
#             question += " ".join([leave for leave in node.leaves()]) + " "
#     question = question[:len(question)-3] + "?"
#     return question

def get_who(tagged):
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

def get_what(tagged):
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



def concat(l):
    if len(l) == 0:
        return ""
    return reduce(lambda a, b: a+" "+b, l)

def get_howmany(sent_tokens, tagged):
    for i in xrange(len(tagged)):
        if tagged[i][1] == "CD":
            for j in xrange(len(tagged[i:])):
                if tagged[i+j][1] == "NNS" or tagged[i+j][1] == "NN":
                    object = tagged[i+1:i+j+1]
                    main_sentence = sent_tokens[:i]
                    if len(main_sentence) > 0:
                        main_sentence[0] = main_sentence[0].lower()
                    break
    question = "How many " + concat(map(lambda x: x[0], object)) + " " + concat(main_sentence)+"?"
    return question

def get_why(sent_tokens, tagged):
    consequence = ""
    for i in xrange(len(tagged)):
        # Case: .(consequence).. because (reason).....
        if tagged[i][0].lower() in ["since", "because", "as"] and ("," not in sent_tokens[i:]):
            consequence = reduce(lambda a, b: a+" "+b, sent_tokens[:i-1])
            break
        # Case: because ..(reason).. , .(consequence)
        elif tagged[i][0].lower() in ["since", "because", "as"] and ("," in sent_tokens[i:]):
            consequence = reduce(lambda a, b: a+" "+b, sent_tokens[sent_tokens.index(",")+1:])
            break
        # other cases: due to ...
    # question = get_binary(consequence, twist=False)
    question = "Why "+consequence+"?"
    return question

# test = "Chris Columbus, the director of the previous two films, decided not to return and helm the third instalment as he \"hadn't seen [his] own kids for supper in the week for about two and a half years.\""
# print get_why(test)

def get_where(sentence, tagged, ners):
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
            while j < len(ners) and (ners[j][0] == "," or ners[j][1] == 'ORGANIZATION' or ners[j][1] == 'LOCATION'):
                j+=1
            if j > i+1:
                for k in xrange(0, j-i):
                    ners.pop(i)
                break

    question = "Where " + ' '.join([w for (w, t) in ners])
    return question.strip()+"?"

def get_when(sentence, tagged, ners):
    first_word = 0
    delete_words = False
    sentence_ners = []

    for i in range(0, len(ners)):
        if tagged[i][0] == 'during':
            j = i+1
            while j < len(ners) and (ners[j][0] == '~' or ners[j][0] == '-' or ners[j][0] != ',' or ners[j][0] != '?'):
                j+=1
            if j > i+1:
                for k in xrange(0, j-i):
                    ners.pop(i)
                    tagged.pop(i)
                break
        if tagged[i][0] == 'since' or tagged[i][0] == 'when' or tagged[i][0] == 'before' or tagged[i][0] == 'after':
            j = i+1
            while j < len(ners) and (ners[j][0] != ',' or ners[j][0] != '?'):
                j+=1
            if j > i+1:
                for k in xrange(0, j-i):
                    ners.pop(i)
                    tagged.pop(i)
                break
        if tagged[i][1] == 'IN':
            j = i+1
            while j < len(ners) and (ners[j][1] == 'DATE' or ners[j][1] == 'TIME'):
                j+=1
            if j > i+1:
                for k in xrange(0, j-i):
                    ners.pop(i)
                    tagged.pop(i)
                break
        if ners[i][1] == 'DATE' or ners[i][1] == 'TIME':
            j = i+1
            while j < len(ners) and (ners[j][1] == 'DATE' or ners[j][1] == 'TIME'):
                j+=1

            if j > i+1:
                for k in xrange(0, j-i):
                    #ners = ners[0:i-1]
                    ners.pop(i)
                    tagged.pop(i)
                break
    if len(ners) < 3:
        return ""
    #print ners

    if (ners[1][0] == 'In' or ners[1][0] == 'On') and (ners[2][1] == 'DATE' and ners[3][1] == 'DATE'):
        ners.pop(1)
        ners.pop(1)
        ners.pop(1)
        tagged.pop(1)
        tagged.pop(1)
        tagged.pop(1)

    elif (ners[1][0] == 'In' or ners[1][0] == 'On') and (ners[2][1] == 'DATE'):
        ners.pop(1)
        ners.pop(1)
        tagged.pop(1)
        tagged.pop(1)
    if (ners[1][0] == ','):
        ners.pop(1)
        tagged.pop(1)

    for k in xrange(len(ners)):
        if first_word == 1 and ners[k][0] != 'PERSON':
            lowered = ners[k][0].lower()
            ners[k] = (lowered, ners[k][1])
            tagged[k] = (lowered, tagged[k][1])
        first_word += 1
        if (ners[k][1] != 'DATE' and delete_words == False):
            sentence_ners.append(ners[k])
        elif (ners[k][1] == 'DATE'):
            delete_words = True
    while (tagged[-1][1] == 'IN' or tagged[-1][1] == 'CC' or tagged[-1][1] == 'DT'):
        sentence_ners.pop(-1)
        tagged.pop(-1)
    question = "When " + ' '.join([w for (w, t) in sentence_ners])+"?"
    return question

