__author__ = 'zhenzhenweng'
import nltk
import nltk.tokenize
import nltk.tag

def concat(l):
    return reduce(lambda a, b: a+" "+b, l)

def generate_number_question(sentence):
    d = nltk.tokenize.word_tokenize(sentence)
    tagged = nltk.tag.pos_tag(d)
    print tagged

    for i in xrange(len(tagged)):
        # Case: .(consequence).. because (reason).....
        if tagged[i][1] == "CD":
            for j in xrange(len(tagged[i:])):
                if tagged[i+j][1] == "NNS" or tagged[i+j][1] == "NN":
                    object = tagged[i+1:i+j+1]
                    main_sentence = d[:i]
                    main_sentence[0] = main_sentence[0].lower()
                    print object
                    break
    output = "How many " + concat(map(lambda x: x[0], object)) + " " + concat(main_sentence)+"?"
    print output


generate_number_question("It contains two stars with known planets.")