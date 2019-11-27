#!/usr/bin/env python

import os,sys,time
from google.cloud import translate_v2
from languages import LANGUAGES_100M, LANGUAGES_GOOGLE
import dotenv, pathlib

class Babelfish:
    ERROR_TIMEOUT=4.0
    def addCommonLanguages(self):
        for language in LANGUAGES_100M:
            self.addLanguage(language)

    def __init__(self,source='English'):
        if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')==None:
            dotenv.load_dotenv(pathlib.Path('.') / '.env')
        self._source = LANGUAGES_GOOGLE[source]
        self._languages = set()
        self._client = None
        self.addCommonLanguages()

    def addLanguage(self,language):
        self._languages.add(LANGUAGES_GOOGLE[language])

    def removeLanguage(self,language):
        self._languages.remove(LANGUAGES_GOOGLE[language])

    def clearLanguages(self):
        self._languages.clear()
    @property
    def source(self):
        return self._source

    @property
    def client(self):
        if self._client == None:
            self._client = translate_v2.Client()
        return self._client

    def close(self):
        if self._client != None:
            self._client = None
        

    def retryingTranslate(self,values,target_language=None,format_=None,source_language=None,customization_ids=(),model=None):
        while True:
            try:
                response=self.client.translate(values,target_language,format_,source_language,customization_ids)
                if response != None:
                    return response
            except:
                print("Unexpected error:", sys.exc_info()[0])
                self.close()
                time.sleep(Babelfish.ERROR_TIMEOUT)

    def translate(self,phrase):
        translations={}
        for target in self._languages:
            if target == self.source:
                translation=phrase
            else:
                response=self.retryingTranslate(phrase, target, None, self.source)
                translation=response['translatedText']
            translations[target]=translation
        return translations
    
def babelfish(*words):
    babelfish = Babelfish()
    try:
        for word in words:
            print(repr(babelfish.translate(word)))
    finally:
        babelfish.close()

def testBabelfish():
    babelfish("pidgin")

def main():
    args = sys.argv
    args.pop(0)
    if len(args) == 0:
        testBabelfish()
    else:
        babelfish(*args)

if __name__ == '__main__':
    main()
