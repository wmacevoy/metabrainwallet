#!/usr/bin/env python

import sys,re
from cachedbabelfish import CachedBabelfish
from bad import Bad
from phrase import Phrase
from languages import LANGUAGES_GOOGLE_INVERSE

class Translator:
    def __init__(self):
        self._count = 0
        self._babelfish=None
        self._reverse = {}
        self.dry = False
        self.verbose = False

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

    @property
    def db(self):
        return self.babelfish.db

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
        self.db.bad.addAll(words)
        words=list(words)
        n = len(words)
        for i in range(n):
            word=words[i]
            self.cache(word)
            print(f"bad word {i} of {n} cached")                        
        print(f"bad words cached")            

    def common(self, maxCount = None):
        phrases=Phrase.getCommon('count_1w100k.txt',maxCount)
        self.db.phrase.addAll(phrases)
        n = len(phrases)
        for i in range(n):
            self.babelfish.db.phrase.save(phrases[i])
            word=phrases[i].content
            self.cache(word)
            print(f"common word {i} of {n} cached")                        
        print(f"common words cached")

    def option(self,result,index,convert,default):
        if result != None:
            groups=result.groups()
            if index < len(groups) and groups[index] != None:
                return convert(groups[index])
        return default
                
    def cli(self,commands):
        for command in commands:
            result = re.match(r"^--?dry(==?(true|false))?$",command)
            if result != None:
                self.dry = self.option(result,1,lambda x: x == "true", True)
                continue
            
            result=re.match(r"^--?verbose(==?(true|false))?$",command)
            if result != None:
                self.verbose = self.option(result,1,lambda x: x == "true", True)
                continue
                
            result=re.match(r"^--?common(==?([0-9]+))?$",command)
            if result != None:
                maxCount = self.option(result,1,lambda x: int(x), None)
                if self.verbose: print(f"common({type(maxCount)} maxCount={maxCount})")                
                if not self.dry: self.common(maxCount)
                continue
                
            result=re.match(r"^--?bad(==?([0-9]+))?$",command)
            if result != None:
                maxCount = self.option(result,1,lambda x: int(x), None)
                if self.verbose: print(f"bad({repr(maxCount)})")                
                if not self.dry: self.bad(maxCount)
                continue

            result=re.match(r"^--?db==?(.*)$",command)
            if result != None:
                dbFile=self.option(result,0,lambda x: str(x), None)
                if self.verbose: print(f"dbFile={dbFile}")
                self.db.dbFile=dbFile
                continue
            
            result=re.match(r"^--?createTables$",command)
            if result != None:
                if self.verbose: print(f"createTables")
                if not self.dry: self.db.createTables()
                continue

            result=re.match(r"^--?dropTables$",command)
            if result != None:
                if self.verbose: print(f"dropTables")
                if not self.dry: self.db.dropTables()
                continue
            
            raise Exception(f"unknown command '{command}'")

def main():
    args = sys.argv
    args.pop(0)
    translator=Translator()
    translator.cli(args)

if __name__ == '__main__':
    main()
