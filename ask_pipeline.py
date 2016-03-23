__author__ = 'rnunez'

import nltk
from nltk.tree import *
from nltk.parse.stanford import StanfordParser
from nltk.grammar import CFG, Nonterminal
import os

input_sentence = 'Between 2007 and 2012, Dempsey played for Premier League team Fulham and is the club\'s highest Premier League goalscorer of all time.'


def pre_process_sentence(input_sentence):
	simple_predicate_check = False
	apposition_check = False
	relative_clause_check = False
	good_sentences = []

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
		if s1[0].label() != 'NP':
			#print s1[0].label()
			s1.pop(0)
		elif s1[0].label() != '.':
			found_NP = True
		else:
			found_NP = True


	if s1.label() == 'S' and s1[0].label() == 'NP' and s1[1].label() == 'VP' and s1[2].label() == '.':
		simple_predicate_check = True
		print "TRUE"

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
					vp_start = vp_start + ' ' + u
				vp_start = np_start + ' ' + vp_start
				good_sentences.append(vp_start)
				print good_sentences
				vp_start = ''
				for h in xrange(len(temp_list)):
					vp_re_list.append(temp_list[h])
			elif(vp_re_counter >= 3):
				vp_repeated = True
			pass
	return good_sentences
