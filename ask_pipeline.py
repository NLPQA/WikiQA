__author__ = 'rnunez'

import nltk
from nltk.tree import *
from nltk.parse.stanford import StanfordParser
from nltk.grammar import CFG, Nonterminal
import os

#input_sentence = 'Between 2007 and 2012, Dempsey played for Premier League team Fulham and is the club\'s highest Premier League goalscorer of all time.'


def pre_process_sentence(input_sentence):
	simple_predicate_check = False
	apposition_check = False
	relative_clause_check = False
	good_sentences = []
	final_sentences = []

	english_parser = StanfordParser("stanford-parser.jar", "stanford-parser-3.4.1-models.jar")
	sentences = english_parser.raw_parse((input_sentence))

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


tests1 =['Starbucks is doing very well lately.',
               'Overall, while it may seem there is already a Starbucks on every corner, Starbucks still has a lot of room to grow.',
               'They just began expansion into food products, which has been going quite well so far for them.',
               'I can attest that my own expenditure when going to Starbucks has increased, in lieu of these food products.',
               'Starbucks is also indeed expanding their number of stores as well.',
               'Starbucks still sees strong sales growth here in the united states, and intends to actually continue increasing this.',
               'Starbucks also has one of the more successful loyalty programs, which accounts for 30%  of all transactions being loyalty-program-based.',
               'As if news could not get any more positive for the company, Brazilian weather has become ideal for producing coffee beans.',
               'Brazil is the world\'s #1 coffee producer, the source of about 1/3rd of the entire world\'s supply!',
               'Given the dry weather, coffee farmers have amped up production, to take as much of an advantage as possible with the dry weather.',
               'Increase in supply... well you know the rules...',]

tests2 = ['Clinton Drew was born March 9, 1983.',
            'Clinton Drew, born March 9, 1983, is an American soccer player who plays for Tottenham Hotspur and the United States national team.',
             'Growing up in Nacogdoches, Texas, Dempsey played for one of the top youth soccer clubs in the state, the Dallas Texans, before playing for Furman University\'s men\'s soccer team. ',
             'In 2004, Dempsey was drafted by Major League Soccer club New England Revolution, where he quickly integrated himself into the starting lineup. ',
             'Hindered initially by a jaw injury, he would eventually score 25 goals in 71 appearances with the Revolution.',
             'Between 2007 and 2012, Dempsey played for Premier League team Fulham and is the club\'s highest Premier League goalscorer of all time.',
             'Dempsey first represented the United States at the 2003 FIFA World Youth Championship in the United Arab Emirates. He made his first appearance with the senior team on November 17, 2004, against Jamaica; he was then named to the squad for the 2006 World Cup and scored the team\'s only goal of the tournament. ',
             'In the 2010 FIFA World Cup, Dempsey scored against England, becoming the second American, after Brian McBride, to score goals in multiple World Cup tournaments.']

testing = ['Increase in supply... well you know the rules...']

def get_final_sentences(input_sentence_list):
	output = []
	for i in input_sentence_list:
		temp_list = pre_process_sentence(i) 
		for sentence in temp_list:
			if (sentence[-1] != '.'):
				sentence = sentence + '.'
			if (sentence[0].isupper() != True):
				sentence[0].upper()
			output.append(sentence)
	return output

#print get_final_sentences(tests)
