#!/usr/bin/env python3

from cachedbabelfish import CachedBabelfish
from bad import Bad
from phrase import Phrase

class Translator:
    def __init__(self):
        self._count = 0
        self._babelfish=None

    @property
    def babelfish(self):
        if self._babelfish == None:
            self._babelfish=CachedBabelfish()
        return self._babelfish

    def close(self):
        if self._babelfish != None:
            self._babelfish.close()
            self._babelfish = None

    def cache(self,word):
        self.babelfish.translate(word)
        self._count = self._count + 1
        if self._count % 1000 == 0:
            print(f"checkpoint word={word} count={self._count}")
            self.close()

    def bad(self):
        words=Bad.getBadWords()
        words=list(words)
        n = len(words)
        for i in range(n):
            word=words[i]
            self.cache(word)
            print(f"bad word {i} of {n} cached")                        
        print(f"bad words cached")            

    def common(self):
        phrases=Phrase.getCommon()
        n = len(phrases)
        for i in range(n):
            word=phrases[i].content
            self.cache(word)
            print(f"common word {i} of {n} cached")                        
        printf(f"common words cached")

def main():
    translator=Translator()
    translator.bad()
    translator.common()
    translatr.close()
    
if __name__ == '__main__':
    main()
