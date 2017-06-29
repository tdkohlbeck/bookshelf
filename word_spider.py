from bs4 import BeautifulSoup
import pprint as p
import re, urllib.request

class BookmarkCorpus:
    def __init__(self, url, crawl_depth=1):
        self.url = url
        self.crawl_depth = crawl_depth

        self.urls = []



    def print_seed_url(self):
        print(self.url)

    def print_crawl_depth(self):
        print(self.crawl_depth)

    def get_words(self):
        html = urllib.request.urlopen(self.url).read()
        soup = BeautifulSoup(html, 'html.parser')
        for elem in soup.find_all(['script', 'style']):
            elem.extract()
        self.urls.append(
            [ link['href'] for link in soup.find_all('a') ]
        )

        with open('stopwords.txt') as sw:
            stopwords = []
            for line in sw.readlines():
                stopwords.append(line[:-1])
        stopwords = set(stopwords)

        words = [
            word for word in soup.get_text().lower().split()
            if word not in stopwords
        ]
        words = [
            re.sub(r'([^a-z]+)', '', word)
            for word in words
        ]
        words = list(filter(None, words))
        p.pprint(words)


bm_corp = BookmarkCorpus('http://google.com', 3)
bm_corp.get_words()

"""
class Hold All Spider Words
what is it you're holding? words (tokens) from bookmark and
links
"""
