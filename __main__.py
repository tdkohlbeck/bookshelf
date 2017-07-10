from bookmark import Bookmark
from webpage import Webpage

bm = Bookmark('https://en.wikipedia.org/wiki/Futurama')
words = bm.get_words()
links = bm.get_links()

for link in links:
    bm = Bookmark(link)
    more_links = bm.get_links()
    if more_links:
        links.extend(more_links)
        print('__________________________________')
        print('  new links: ' + str(len(more_links)))
        print('total links: ' + str(len(links)))
        print('  avg links: ' + str(bm.link_avg()))
        print('  std links: ' + str(bm.link_std()))
    if len(links) > 1000: break

for link in links:
    bm = Bookmark(link)
    more_words = bm.get_words()
    if more_words:
        words.extend(more_words)
        print('__________________________________')
        print('  new words: ' + str(len(more_words)))
        print('total words: ' + str(len(words)))
        print('  avg words: ' + str(bm.word_avg()))
        print('  std words: ' + str(bm.word_std()))

bm.get_bow(words)

"""
NOTES:

class Hold All Spider Words
what is it you're holding? words (tokens) from bookmark and
links
"""
