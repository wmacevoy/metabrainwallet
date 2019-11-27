#!/usr/bin/env python3

from cachedbabelfish import CachedBabelfish
from bad import Bad
from phrase import Phrase
from languages import LANGUAGES_GOOGLE_INVERSE

class Translator:
    def __init__(self):
        self._count = 0
        self._babelfish=None
        self._reverse = {}

    def reverse(self,language):
        if not language in self._reverse:
            reverse=CachedBabelfish(source = language)
            reverse.db.dbFile = self._babelfish.db.dbFile
            reverse.clearLanguages()
            reverse.addLanguage("English")
            self._reverse[language] = reverse
        return self._reverse[language]

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
        response=self.babelfish.translate(word)
        for code in response:
            language = LANGUAGES_GOOGLE_INVERSE[code]
            phrase = response[code]
            back=self.reverse(language).translate(phrase)
        self._count = self._count + 1
        if self._count % 1000 == 0:
            print(f"checkpoint word={word} count={self._count}")
            self.close()

    def bad(self, maxCount = None):
        words=Bad.getBadWords(maxCount)
        words=list(words)
        n = len(words)
        for i in range(n):
            word=words[i]
            self.cache(word)
            print(f"bad word {i} of {n} cached")                        
        print(f"bad words cached")            

    def common(self, maxCount = None):
        phrases=Phrase.getCommon('count_1w100k.txt',maxCount)
        n = len(phrases)
        for i in range(n):
            self.babelfish.db.phrase.save(phrases[i])
            word=phrases[i].content
            self.cache(word)
            print(f"common word {i} of {n} cached")                        
        print(f"common words cached")

def main():
    translator=Translator()
    translator.bad()
    translator.common()
    translator.close()

    
if __name__ == '__main__':
    main()
