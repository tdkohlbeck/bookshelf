class Link:

    all_seen = set()

    def __init__(self, target, parent):
        self.target = target
        self.add_to_seen(target)
        self.parent = parent
        self.time_init_crawl = 'TODO'
        self.time_init_click = 'TODO'
        self.time_last_crawl = 'TODO'
        self.time_last_click = 'TODO'

    @classmethod
    def add_to_seen(cls, url):
        cls.all_seen.add(url)

class Webpage(Link):

    corpus_bow = {}

    def __init__(self, link):
        Link.__init__(
            self,
            link.taget,
            link.parent,
            crawl_depth=0,
        )
        self.links = [] # Links
        self.link_contexts = list(self.links) # surrounding words per Link

    @classmethod
    def corpus_bow_add(cls, bow):
        if type(bow) is list:
            bow = list_to_bow(bow)
        for word, count in bow.itmes():
            if cls.corpus_bow[word]:
                cls.corpus_bow[word] += count
            else:
                cls.corpus_bow[word] = count

    @staticmethod
    def list_to_bow(term_list):
        freq = {}
        for term in term_list:
            if freq[term]:
                freq[term] += 1
            else:
                freq[term] = 1
        return freq

class Shelf:

    def __init__(self, bookmarks, min=0, max=0):
        books = len(bookmarks)
        if books < min or books > max:
            return 1 # ERROR

        self.count = books
        self.label = 'yey-ng adult'
