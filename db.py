import os,sys,sqlite3,datetime
from badtable import BadTable
from phrasetable import PhraseTable
from translationtable import TranslationTable
from __future__ import print_function

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class Db:
    DEFAULT_DB_FILE = str(os.path.expanduser("metabrainwallet.db"))
    DEFAULT_SLOW = 1.0

    def __init__(self, dbFile=DEFAULT_DB_FILE):
        self._connection = None
        self._bad = BadTable(self)
        self._phrase = PhraseTable(self)
        self._translation = TranslationTable(self)
        self._dbFile = dbFile
        self._slow = DEFAULT_SLOW

    @property
    def bad(self):
        return self._bad

    @property
    def phrase(self):
        return self._phrase

    @property
    def translation(self):
        return self._translation
    
    @property
    def dbFile(self):
        return self._dbFile

    @dbFile.setter
    def dbFile(self, value):
        if self._connection != None:
            raise ValueError('connection is already open.')

        if value.startswith("/"):
            self._dbFile = value
        else:
            dir = os.path.dirname(os.path.realpath(__file__))
            self._dbFile = dir + "/" + value

    @property
    def connection(self):
        if self._connection == None:
            self._connection = sqlite3.connect(self._dbFile)
            self.createTables()
        return self._connection

    def cursor(self):
        return self.connection.cursor()

    def execute(self,sql,parameters=None):
        if parameters != None:
            cursor=self.cursor()
            t0 = datetime.datetime.now()
            cursor.execute(sql,parameters)
            t1 = datetime.datetime.now()            
            delta = (t1 - t0).total_seconds()
            if delta > self.slow:
                print(f"slow: {sql} parameters={repr(parameters)} in {delta}s")
            return cursor
        else:
            cursor=self.cursor()
            t0 = datetime.datetime.now()
            cursor.execute(sql)
            t1 = datetime.datetime.now()            
            delta = (t1 - t0).total_seconds()
            if delta > self.slow:
                print(f"slow: {sql} in {delta}s")
            return cursor

    def createTables(self):
        self.bad.createTable()
        self.phrase.createTable()
        self.translation.createTable()

    def dropTables(self):
        self.bad.dropTable()
        self.phrase.dropTable()
        self.translation.dropTable()

    def close(self):
        if not self._connection == None:
            self._connection.commit()
            self._connection.close()
        self._connection = None

def main():
    db=Db()
    db.dropTables()
    db.createTables()
    db.bad.addBadWords()
    db.phrase.addCommon()
    db.close()

if __name__ == '__main__':
    main()
