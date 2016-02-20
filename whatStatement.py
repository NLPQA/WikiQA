import nltk

def whatQuesGen(sentence):
    words = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(words)
    NN = []
    start = 0
    for i in range(0, len(tagged)):
        if tagged[i][0] == 'is' or tagged[i][0] == 'are':
            start = i
            break;
        if tagged[i][1][0:2] == 'NN':
            NN.append(tagged[i][0])
    question = 'What '
    for j in range(start, len(tagged)):
        if j < len(tagged) - 2:
            question += tagged[j][0] + ' '
        elif j >= len(tagged) - 2 and tagged[j][0] != '.':
            question += tagged[j][0]
        else:
            question += '?'
    answer = ''
    if len(NN) == 1:
        answer = NN[0]
    else:
        for i in range(0,len(NN)-1):
            answer += NN[i] + ', '
        answer = answer[:-2]
        answer += ' and ' + NN[-1]
    print question + ' ' + answer



test1 = 'Python is a scripting language.'
test2 = 'Both Earth and Mars are in solar system.'
test3 = 'Banana, apple, grapes and oranges are all my favorite fruits.'
# whatQuesGen(test1)
# whatQuesGen(test2)
whatQuesGen(test3)