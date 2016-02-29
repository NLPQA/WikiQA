__author__ = 'zhenzhenweng'
import nltk
import nltk.tokenize
import nltk.tag

def generate_helping_verb_question(sentence):
    holder = ('', '')
    output = ''
    tagged = nltk.pos_tag(nltk.word_tokenize((sentence)))
    print tagged
    #We now iterate through the tuples in order to find the following rules:
    #1) if POS is 'MD'
    #2) if word is 'have'
    #3) if word is 'has' and part of speech is 'VBZ'
    #Then we make the word in the first tuple lowercase and mover the tuple
    #with the helping verb to the front

    for i in xrange(len(tagged)):
        if (tagged[i][1] == 'MD' or tagged[i][0] == 'have' or (tagged[i][0] == 'has' and tagged[i][1] == 'VBZ')):
            if tagged[0][1] != 'NNP' or tagged[0][1] != 'NNPS':
                holder = (tagged[0][0].lower(), tagged[0][1])
                tagged[0] = holder
            tagged.insert(0, tagged.pop(i))

    #Now we iterate through the modified list and add each word to string 'output'
    #We only add spaces up until the second to last character
    #Then instead of a period, we add a question mark

    for j in xrange(len(tagged)):
        if j < len(tagged) - 2:
            output += tagged[j][0] + ' '
        elif j >= len(tagged) - 2 and tagged[j][0] != '.':
            output += tagged[j][0]
        else:
            output += '?'
    return output

def generate_why_question(sentence):
    d = nltk.tokenize.word_tokenize(sentence)
    tagged = nltk.tag.pos_tag(d)
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
    output = generate_helping_verb_question(consequence+"?")
    output = "Why "+output
    print output


def concat(l):
    return reduce(lambda a, b: a+" "+b, l)


generate_why_question("He attended church every week with his parents, because that was the only way he could play football for their team.")