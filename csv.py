#!/usr/bin/env python
from db import Db
class CSV:
    def __init__(self):
        self.db = Db()
        self.csvFileName = "translation.csv"


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
        print("frequency,englishWord,translatedLanguage,translatedPhrase,translatedPhraseInEnglish",file=csv)
        for row in cursor:
            (frequency,englishWord,translatedLanguage,translatedPhrase,translatedPhraseInEnglish,)=row
            print(f"{frequency},{englishWord},{translatedLanguage},{translatedPhrase},{translatedPhraseInEnglish}",file=csv)
        csv.close()

def main():
    csv = CSV()
    csv.generate()

if __name__ == '__main__':
    main()
