__author__ = 'laceyliu'

dir = "/Users/laceyliu/Documents/workspace/"
parser_path = dir + 'WikiQA/stanford-parser-full/'
ner_path = dir+'WikiQA/stanford-ner'
which_java = '/Library/Java/JavaVirtualMachines/jdk1.8.0_25.jdk/Contents/HOME/bin/java'

import os
from nltk.parse.stanford import StanfordParser
from nltk.tag.stanford import StanfordNERTagger
def new_parser():
    os.environ['JAVAHOME'] =  which_java
    os.environ['CLASSPATH'] = parser_path
    os.environ['STANFORD_MODELS'] = parser_path
    return StanfordParser()

def new_NERtagger():
    os.environ['JAVAHOME'] =  which_java
    return StanfordNERTagger(ner_path+'/classifiers/english.muc.7class.distsim.crf.ser.gz', ner_path+ '/stanford-ner-3.5.2.jar')
