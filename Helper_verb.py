import nltk


def helping_verb_statements(statement):
	text = statement
	sent  =  nltk.sent_tokenize(text)
	holder = ('','')
	output = ''
	moved_already = False

	#Here we are making a list of tuples containing (word, POS)
	#we are storing this list in variable named 'tagged'

	for s in sent:
		d = nltk.word_tokenize(s)
	tagged = nltk.pos_tag(d)
	#print tagged

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
			tagged.insert(0,tagged.pop(i))

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
	print output

helping_verb_statements("The firemen have saved the kitten.")
helping_verb_statements("The dogs will bark if they see cats.")
helping_verb_statements("David Beckham has got a nice car.")
helping_verb_statements("Cristiano Ronaldo has had 7 division titles.")
helping_verb_statements("Their use and control have been a major focus of international relations policy since their debut.")
#Atomic bombs wiki article



