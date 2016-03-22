__author__ = 'laceyliu'

parser_path ='/Users/laceyliu/Documents/workspace/WikiQA/stanford-parser-full'
which_java = '/Library/Java/JavaVirtualMachines/jdk1.8.0_11.jdk/Contents/HOME/bin/java'
import os
from nltk.parse.stanford import StanfordParser
os.environ['JAVAHOME'] =  which_java
os.environ['CLASSPATH'] = parser_path
os.environ['STANFORD_MODELS'] = parser_path
sentence = "hello world"
sp=StanfordParser()

sentences = ['Clinton Drew \"Clint\" Dempsey (born March 9, 1983) is an American soccer player who plays for Tottenham Hotspur and the United States national team.',
             'Growing up in Nacogdoches, Texas, Dempsey played for one of the top youth soccer clubs in the state, the Dallas Texans, before playing for Furman University\'s men\'s soccer team. ',
             'In 2004, Dempsey was drafted by Major League Soccer club New England Revolution, where he quickly integrated himself into the starting lineup. ',
             'Hindered initially by a jaw injury, he would eventually score 25 goals in 71 appearances with the Revolution.',
             'Between 2007 and 2012, Dempsey played for Premier League team Fulham and is the club\'s highest Premier League goalscorer of all time.',
             'Dempsey first represented the United States at the 2003 FIFA World Youth Championship in the United Arab Emirates. He made his first appearance with the senior team on November 17, 2004, against Jamaica; he was then named to the squad for the 2006 World Cup and scored the team\'s only goal of the tournament. ',
             'In the 2010 FIFA World Cup, Dempsey scored against England, becoming the second American, after Brian McBride, to score goals in multiple World Cup tournaments.']

ss2 = []
for s in sentences:
    if s.count(' ') < 20 and s.count(' ') > 7:
        ss2.append(s.decode('utf-8').encode('ascii', 'ignore'))
trees = sp.raw_parse_sents(ss2)
for t in trees:
    print list(t)
