#!/usr/bin/env python3

from unittest import TestCase, main
from cachetranslations import Translator

class TestCacheTranslations(TestCase):
    def testTranslate(self):
        translator=Translator()
        translator.babelfish.db.dbFile = "test.db"
        translator.babelfish.db.dropTables()
        translator.babelfish.db.createTables()    
        translator.bad(2)
        translator.common(3)
        translator.close()

if __name__ == '__main__':
    main()
    
