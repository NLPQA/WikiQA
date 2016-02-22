__author__ = 'laceyliu'
import nltk
import stanford_utils
def binaryQuesGen(sentence):
    sent = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(sent)
    question = ""

    for i in xrange(len(tagged)):

        if tagged[i][1] == 'MD' or tagged[i][0] == 'have' or (tagged[i][0] == 'has' and tagged[i][1] == 'VBZ') or tagged[i][0] == 'am'  or tagged[i][0] == 'are' or (tagged[i][0] == 'is' and tagged[i][1] == 'VBZ'):
            if tagged[0][1] != 'NNP' or tagged[0][1] != 'NNPS':
                tagged[0] = (tagged[0][0].lower(), tagged[0][1])
            tagged.insert(0, tagged.pop(i))
            break
        elif tagged[i][1] == 'VBD':
            tagged[i] = (tagged[i][0][:-2], 'VB')
            if tagged[0][1] != 'NNP' or tagged[0][1] != 'NNPS':
                tagged[0] = (tagged[0][0].lower(), tagged[0][1])
            tagged.insert(0, ('did', 'MD'))
            break
        elif tagged[i][1] == 'VBZ':
            tagged[i] = (tagged[i][0][:-1], 'VB')
            if tagged[0][1] != 'NNP' or tagged[0][1] != 'NNPS':
                tagged[0] = (tagged[0][0].lower(), tagged[0][1])
            tagged.insert(0, ('Does', 'MD'))
            break


    for j in xrange(len(tagged)):
        if j < len(tagged) - 2:
            question += tagged[j][0] + ' '
        elif j >= len(tagged) - 2 and tagged[j][0] != '.':
            question += tagged[j][0]
        else:
            question += '?'
    return question


def whereQuesGen(sentence):

    binary_q = binaryQuesGen(sentence)

    words = nltk.word_tokenize(binary_q)
    tagger = stanford_utils.new_NERtagger()
    ners = tagger.tag(words)
    tagged = nltk.pos_tag(words)

    for i in range(0, len(ners)):
        if tagged[i][0] == 'where':
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
    return question

def whenQuesGen(sentence):

    binary_q = binaryQuesGen(sentence)

    words = nltk.word_tokenize(binary_q)
    tagger = stanford_utils.new_NERtagger()
    ners = tagger.tag(words)
    tagged = nltk.pos_tag(words)

    for i in range(0, len(ners)):
        if tagged[i][0] == 'during':

            while j < len(ners) and (ners[j][0] == '~' or ners[j][0] == '-' or ners[j][0] != ',' or ners[j][0] != '?'):
                j+=1
            if j > i+1:
                for k in xrange(0, j-i):
                    ners.pop(i)
                break

        if tagged[i][0] == 'since' or tagged[i][0] == 'when' or tagged[i][0] == 'before' or tagged[i][0] == 'after':
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




    question = "When " + ' '.join([w for (w, t) in ners])+"?"
    return question



test = "The scientist worked at Carnegie Mellon University during 1990 - 1991."
# print whenQuesGen(test)
# print whereQuesGen(test)
# test1 ="Python is a scripting language."
# print binaryQuesGen(test1)

tagger = stanford_utils.new_NERtagger()
print tagger.tag(test.split())


