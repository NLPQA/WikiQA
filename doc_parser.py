__author__ = 'laceyliu'
from bs4 import BeautifulSoup
from nltk import tokenize
import string
from nltk.corpus import wordnet as wn

cur_article = ""
content = ""
vocab = {}
idfs = {}
sentences = []
vects = []

stopwords = []
with open('stopwords.txt') as sf:
    stopwords = sf.read().splitlines()
sf.close()

def clear(article):
    if article != cur_article:
        content = doc_to_string(article)
        vocab = {}
        idfs = {}
        sentences = []
        vects = []

def doc_to_sents(article):
    global sentences, cur_article, vocab, idfs, vects
    if article != cur_article:
        content = doc_to_string(article)
        vocab = {}
        idfs = {}
        sentences = []
        vects = []
    sentences = tokenize.sent_tokenize(content)
    return sentences

def doc_to_string(article):
    global content, cur_article
    with open(article) as f:
      soup = BeautifulSoup(f, "html.parser")
    f.close()
    # get rid of citations like "[1]", etc.
    for citation in soup.find_all('sup'):
      citation.decompose()
    # all the useful info in wiki articles are in <p> tags
    paragraphs = soup.find_all('p')
    # combine paragraphs, segment sentences, and parse into Trees
    paragraphs_text = [p.get_text() for p in paragraphs]
    content = ' '.join(paragraphs_text)
    content = content.encode('ascii', 'ignore')
    cur_article = article
    return content

def doc_to_vocab(article):
    global vocab
    if cur_article != article:
        doc_to_string(article)
        doc_to_sents(article)

    for sent in sentences:
        tokens = tokenize.word_tokenize(sent)

        for token in tokens:
            #token = stemmer.stem(token).encode('ascii', 'ignore')

            token = wn.morphy(token)
            if token == None:
                continue
            else:
               token = token .encode('ascii', 'ignore')

            if not vocab.has_key(token):
                vocab[token] = 1
            else:
                vocab[token] += 1
    return vocab

def sent_to_vect(sent):
    vect = {}
    sent = sent.translate(None, string.punctuation)
    tokens = tokenize.word_tokenize(sent)
    tokens = filter(None, tokens)
    for token in tokens:
        # if token in stopwords:
        #     continue
        token = wn.morphy(token)
        if token == None:
            continue
        else:
            token = token.encode('ascii', 'ignore')

        #token = stemmer.stem(token).encode('ascii', 'ignore')

        if token in vect.keys():
            vect[token] += 1
        else:
            vect[token] = 1
    return vect


def doc_to_vects(article):
    global vects
    if cur_article != article:
        doc_to_string(article)
        doc_to_sents(article)
    for sent in sentences:
        vects.append(sent_to_vect(sent))
    return vects

def doc_to_idfs(article):
    global idfs
    if cur_article != article:
        doc_to_string(article)
        doc_to_sents(article)
        doc_to_vocab(article)
    if len(vocab) == 0:
        doc_to_vocab(article)
    for token in vocab.keys():
        for sent in vects:
            if token in sent.keys():
                if idfs.has_key(token):
                    idfs[token] += 1
                else:
                    idfs[token] = 1
    idfs = {token : 1.0/value for token, value in idfs.items()}
    return idfs

# import gold_standard_parser
# test = gold_standard_parser.findPath("Slumdog_Millionaire")
#print "=== Vocab===="
#print doc_to_vocab('a8.htm')
# print "=== Vects===="
# print doc_to_vects(test)
# print "=== IDF===="
# print doc_to_idfs(test)