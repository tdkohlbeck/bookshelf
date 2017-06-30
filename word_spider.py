from collections import defaultdict
from bs4 import BeautifulSoup
import pprint as p
import operator, re, urllib.request

class Bookmark:
    def __init__(self, url):
        self.url = url

        self.crawl_depth = 0
        try:
            self.html = urllib.request.urlopen(self.url)
            self.soup = BeautifulSoup(self.html, 'html.parser')
            for elem in self.soup.find_all(['script', 'style']):
                elem.extract()
        except:
            #print('cannot GET ' + self.url)
            self.html = None
            self.soup = None

    def get_links(self, url=None):
        url = url or self.url
        if not self.soup:
            return []
        return [
            link.get('href') for link in self.soup.find_all('a')
        ]

    def get_stopwords(self, location='stopwords.txt'):
        with open(location) as f:
            return set([
                line[:-1] # except newline
                for line in f.readlines()
            ])

    def print_seed_url(self):
        print(self.url)

    def print_crawl_depth(self):
        print(self.crawl_depth)

    def get_words(self, url=None):
        if not self.soup:
            return []
        stopwords = self.get_stopwords()
        #print(stopwords)

        words = [
            word for word in self.soup.get_text().lower().split()
            if word not in stopwords
        ]
        words = [
            re.sub(r'([^a-z]+)', '', word)
            for word in words
        ]
        words = list(filter(None, words))
        #p.pprint(words)

        return words

    def get_bow(self, words):
        freq = defaultdict(int)
        for word in words:
            freq[word] += 1
            print(str(freq[word]) + " " + word)
        p.pprint(sorted(freq.items(), key=operator.itemgetter(1)))

bm = Bookmark('https://www.crummy.com/software/BeautifulSoup/bs4/doc/#')
words = bm.get_words()
links = bm.get_links()
print(len(links))
for link in links:
    bm = Bookmark(link)
    links.extend(bm.get_links())
    print('links: ' + str(len(links)))
    if len(links) > 50000: break
for link in links:
    bm = Bookmark(link)
    words.extend(bm.get_words())
    print('words: ' + str(len(words)))
bm.get_bow(words)
"""
class Hold All Spider Words
what is it you're holding? words (tokens) from bookmark and
links
"""
