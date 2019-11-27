#!/usr/bin/env python3

from unittest import TestCase, main
import datetime,hashlib
from hash import Hash
from bad import Bad
from phrase import Phrase

def hash(str):
    return Hash.hashString(str)

class Collider:
    def __init__(self):
        self.words={}
        self.hashes={}
        self.collisions=set()
    def add(self,word):
        if not word in self.words:
            hash=Hash.hashString(word)
            self.words[word]=hash
            if not hash in self.hashes:
                self.hashes[hash]=set()
                self.hashes[hash].add(word)
            else:
                self.hashes[hash].add(word)
                self.collisions.add(hash)
    def ok(self):
        for hash in self.collisions:
            print(f"{repr(self.hashes[hash])}=>{hash}")
        if (len(self.collisions)>0):
            raise AssertionError("hash has collisions")
        
class TestHash(TestCase):
    def testNone(self):    
        word=None
        expect=None
        result=hash(word)
        self.assertEqual(expect,result)

    def testEmpty(self):
        word=""
        expect=245048209962137
        result=hash(word)
        self.assertEqual(expect,result)

    def testTest(self):
        word="test"
        expect=131165637339759
        result=hash(word)
        self.assertEqual(expect,result)

    def testCollision(self):
        collider=Collider()
        common=Phrase.getCommon()
        for phrase in common:
            word=phrase.content
            collider.add(word)
        badWords=Bad.getBadWords()
        for word in badWords:
            collider.add(word)
        collider.ok()

    def testTime(self):
        phrases=Phrase.getCommon()
        words=set()
        for phrase in phrases:
            words.add(phrase.content)
        h1={}
        t0 = datetime.datetime.now()
        for word in words:
            h1[word]=hash(word)
        t1 = datetime.datetime.now()
        d1 = (t1 - t0).total_seconds()

        h2={}
        t0 = datetime.datetime.now()
        for word in words:
            m = hashlib.sha256()
            utf8=bytes(str(word),'utf-8')            
            m.update(utf8)
            h2[word]=m.digest()
        t1 = datetime.datetime.now()
        d2 = (t1 - t0).total_seconds()

        print(f"ratio={d1/d2}")
        
        
        
        

if __name__ == '__main__':
    main()
