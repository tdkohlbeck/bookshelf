from pprint import pprint
from collections import defaultdict
from bs4 import BeautifulSoup
from gensim import corpora, models, similarities
import urllib.request
import logging
from time import sleep

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
with open('bookmarks.html', 'r') as f:
    soup = BeautifulSoup(f, 'html.parser')

urls = [ link.get('href') for link in soup.find_all('a') ]

DOC_COUNT = 50
docs = []
for x in range(0, DOC_COUNT):
    test_url = urls[x]
    try:
        print('trying ' + test_url)
        test_html = urllib.request.urlopen(test_url).read()
        soup = BeautifulSoup(test_html, 'html.parser')
        [s.extract() for s in soup('script')]
        [s.extract() for s in soup('style')]
        docs.append(soup.get_text())
    except:
        print('could not GET ' + test_url)


stoplist = set('for a of the and to in at can - your i so should it\'s but { we each it that / '.split())
docs = [
    [ word for word in document.lower().split() if word not in stoplist ]
    for document in docs
]

freq = defaultdict(int)
for doc in docs:
    for word in doc:
        freq[word] += 1

docs = [
    [ word for word in doc if freq[word] > 1 ]
    for doc in docs
]

dictionary = corpora.Dictionary(docs)

corpus = [ dictionary.doc2bow(doc) for doc in docs ]

tfidf = models.TfidfModel(corpus)
tfidf_corpus = tfidf[corpus]

lsi = models.LsiModel(tfidf_corpus, id2word=dictionary, num_topics=2)
lsi_corpus = lsi[tfidf_corpus]
lsi.print_topics(2)
