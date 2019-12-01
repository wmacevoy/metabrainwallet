#!/usr/bin/env python
import re
from db import Db
from languages import LANGUAGES_100M

def norm(word):
    return word.lower().replace("&#39;","'") if word != None else None
    
class Word:
    def __init__(self,csv):
        self.current=None
        self.matcher=None
        self.same=0
        self.similar=0
        self.csv = csv
        self.phrases={}

    def hasVowel(self):
        for vowel in ['a','e','i','o','u','y']:
            if self.current.find(vowel) >= 0:
                return True
        return False

    def isSimilar(self):
        similar = True
        sameLanguages=self.phrases[self.current]
#        some=False
        for language in [ "zh-CN", "zh-TW", "hi", "es" ]:
            # these languages translate the word into a phrase that translates back into the word
            similar = similar and (language in sameLanguages)
#            if similar and sameLanguages[language] != self.current:
#                some = True
        # spanish se languages translate the word into a phrase different than the original word
        similar = similar and sameLanguages['es'] != self.current
        similar = similar and self.same >= len(LANGUAGES_100M)
        similar = similar and self.similar >= len(LANGUAGES_100M)
        similar = similar and len(self.current)<=8        
#        similar = similar and len(self.current)>2 and len(self.current)<=8
#        similar = similar and self.hasVowel()
#        similar = similar and not self.current in Word.ODD
#        similar = similar and self.frequency >= 1500000
        
        return similar
    
    def setup(self,current,frequency):
        if self.current != None and self.isSimilar():
            equiv = []
            for phrase in self.phrases:
                langs=list(self.phrases[phrase].keys())
                langs.sort()
                equiv.append(phrase + "(" + ",".join(langs) + ")")
            allPhrases="&".join(equiv)
            print(f"{self.frequency},{self.current}",file=self.csv)
        self.current=norm(current)
        self.frequency=int(frequency) if frequency != None else None
        self.matcher=re.compile(r'\b%s' % self.current, re.I) if current != None else None
        self.same=0
        self.similar=0
        self.phrases={}
        if current != None:
            self.addTranslation('en',self.current,self.current)

    def addTranslation(self,language,translated,phrase):
        phrase = norm(phrase)
        if not phrase in self.phrases:
            self.phrases[phrase]={}
        self.phrases[phrase][language]=translated
        if self.current == phrase:
            self.same += 1
            self.similar += 1
        elif self.matcher != None and self.matcher.search(phrase) != None:
            self.similar += 1

class CSV:
    def __init__(self):
        self.db = Db()
        self.csvFileName = "same.csv"

    def generate(self):
        sql = f"""
        select original.frequency,original.content,translated1.language,translated1.content,translated2.content
        from phrase original
            join translation t1 on original.id = t1.originalId
            join phrase translated1 on t1.translatedId = translated1.id
            join translation t2 on t2.originalId = translated1.id
            join phrase translated2 on t2.translatedId = translated2.id
        where original.language = 'en' and translated2.language = 'en' and original.frequency > 0
        order by original.frequency DESC,original.content,translated1.language
        """
        cursor = self.db.execute(sql)
        csv = open(self.csvFileName,mode="w", encoding="utf-8")
        word = Word(csv)
        print("frequency,englishWord,same,similar,phrases",file=csv)
        for row in cursor:
            (frequency,englishWord,translatedLanguage,translatedPhrase,translatedPhraseInEnglish,)=row
            if word.current != englishWord:
                word.setup(englishWord,frequency)
            word.addTranslation(translatedLanguage,translatedPhrase,translatedPhraseInEnglish)
        word.setup(None,None)
        csv.close()

def main():
    csv = CSV()
    csv.generate()

if __name__ == '__main__':
    main()
