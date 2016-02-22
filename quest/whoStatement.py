import nltk

def generateAns(s, NNP):
    if s[1] == 'NNP':
        NNP.append(s[0])
        return s[0]
    else:
        return NNP[len(NNP) - 1]

def whoQuesGen(test):
    # tokenize into sentences
    sentences = nltk.sent_tokenize(test)
    words = []
    # tokenize into words for each sentence
    for sentence in sentences:
        words.append(nltk.word_tokenize(sentence))
    # tag for words in each sentence
    tagged = []
    for tokenedSen in words:
        tagged.append(nltk.pos_tag(tokenedSen))
    NNP = []
    questions = []
    answers = []
    for tagSen in tagged:
        for i in range(0,len(tagSen)):
            question = ''
            start = 0
            if (tagSen[i][1] == 'MD' or tagSen[i][1] == 'VBD' or tagSen[i][1] == 'VBZ' or tagSen[i][0] == 'has' or tagSen[i][1] == 'is'):
                if tagSen[i][1] == 'MD':
                    start = 1
                    question += 'Who '
                elif tagSen[i][0] == 'has':
                    if tagSen[i+1][1][0:1] == 'V':
                        question += 'Who has '
                        start = i + 1
                    else:
                        question += 'Who does have '
                        start = i + 1
                elif tagSen[i][0] == 'is':
                    question += 'Who is '
                    start = i + 1
                elif tagSen[i][1] == 'VBD':
                    verb = tagSen[i][0][:-2]
                    question += 'Who did ' + verb + ' '
                    start = i + 1
                elif tagSen[i][1] == 'VBZ':
                    verb = tagSen[i][0][:-1]
                    question += 'Who does ' + verb + ' '
                    start = i + 1
                answers.append(generateAns(tagSen[0], NNP))
                for j in range(start,len(tagSen)):
                    if j < len(tagSen) - 2:
                        question += tagSen[j][0] + ' '
                    elif j >= len(tagSen) - 2 and tagSen[j][0] != '.':
                        question += tagSen[j][0]
                    else:
                        question += '?'
                questions.append(question)
                break
    # print out the Q & A
    for i in range(0, len(questions)):
        print questions[i] + " " + answers[i]

test = "Jim is a student. He should go to school. He jumped into the bed instead. He wants more sleep. Tom is the friend of Jim. He has a phone in his hand. He is calling Jim to come to school."
whoQuesGen(test)