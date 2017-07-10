from collections import defaultdict
from bs4 import BeautifulSoup
import pprint as p
import operator, re, urllib.request



class Bookmark:
    link_counts = [] # index per mark
    word_counts = [] # index per mark
    mark_count = 0

    def __init__(
        self,
        url,
        crawl_depth=0,
        link_limit=None,
        word_limit=None,
    ):
        self.url = url
        self.crawl_depth = crawl_depth
        self.link_limit = link_limit
        self.word_limit = word_limit

        # TODO: tidy up, think in terms of responsibility,
        #       and loop for depth in range(0, drawl_depth)
        try:
            self.html = urllib.request.urlopen(self.url)
            self.soup = BeautifulSoup(self.html, 'html.parser')
            for elem in self.soup.find_all(['script', 'style']):
                elem.extract()
        except:
            self.html = None
            self.soup = None

        if self.soup: self.inc_mark_count()

    @staticmethod
    def get_stopwords(location='stopwords.txt'):
        with open(location) as f:
            return set([
                line[:-1] # except newline at end
                for line in f.readlines()
            ])

    @classmethod
    def add_link_count(cls, link_count):
        if link_count: cls.link_counts.append(link_count)

    @classmethod
    def add_word_count(cls, word_count):
        if word_count: cls.word_counts.append(word_count)

    @classmethod
    def inc_mark_count(cls):
        cls.mark_count += 1

    @classmethod
    def link_avg(cls):
        if not cls.mark_count:
            return 0
        return sum(cls.link_counts) / cls.mark_count

    @classmethod
    def word_avg(cls):
        if not cls.mark_count:
            return 0
        return sum(cls.word_counts) / cls.mark_count

    @classmethod
    def link_std(cls):
        return (sum([
            (link_count - cls.link_avg())**2
            for link_count in cls.link_counts
        ]) / cls.mark_count)**(1/2)

    @classmethod
    def word_std(cls):
        return (sum([
            (word_count - cls.word_avg())**2
            for word_count in cls.word_counts
        ]) / cls.mark_count)**(1/2)

    def get_links(self):
        if not self.soup:
            return [ 0 ]
        links = [
            link.get('href')
            for link in self.soup.find_all('a')
        ]
        self.add_link_count(len(links))
        return links

    def get_words(self):
        if not self.soup:
            return [ 0 ]
        stopwords = Bookmark.get_stopwords()
        words = [
            re.sub(r'([^a-z]+)', '', word)
            for word in self.soup.get_text().lower().split()
            if word not in stopwords
        ]
        if len(words) == 1:
            print(self.url)
        self.add_word_count(len(words))
        return list(filter(None, words))

    def get_bow(self, words):
        freq = defaultdict(int)
        for word in words:
            freq[word] += 1
            print(str(freq[word]) + " " + str(word))
        p.pprint(sorted(freq.items(), key=operator.itemgetter(1)))
