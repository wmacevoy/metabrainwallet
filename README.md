# MetaBrainWallet

Meta Brain Wallet has a goal of making a corpus of words suitable for passphrase generation that is somewhat human language agnostic.

## Phase 0 Dataset

- count_1w100k.txt - 100k most popular english words according to http://norvig.com/ngrams (along with a corpus frequency)
- bad_words.txt bad word list according to
https://www.cs.cmu.edu/~biglou/resources/bad-words.txt
- popular laguages (spoken by 100M or more according to ethnologue.com)

|Language             |Code |
|---------------------|-----|
|English              |en   |
|Chinese (Simplified) |zh-CN|
|Chinese (Traditional)|zh-TW|
|Hindi                |hi   |
|Spanish              |es   |
|French               |fr   |
|Arabic               |ar   |
|Bengali              |bn   |
|Russian              |ru   |
|Portuguesed          |pt   |
|Indonesian           |id   |
|Urdu                 |ur   |
|German               |de   |
|Japanese             |jw   |


## Phase 1 Dataset

A word from the common english list is acceptable if 

    The translation to each of the common languages (according to google translate) is a phrase, that, when translated back to english and converted to lower case, is the original word.

## Sqlite Dataset

To facilitate exploration, a dataset is cached as a sqlite datebase:

### phrase
|id|language|content|frequency
|----|----|----|----|
|int|text|text|int or null|

### bad
|id|word|
|----|----|
|int|text|

Instead of the original word, a simple hash of the word is stored instead (based on rand48).  The hash is tested to have no collisions for the union of the 100k and bad-words list.

### translate
|id|originalId|translatedId|
|---|---|---|
|int|int (phrase id)|int (phrase id)|

The `CachedBabelfish` looks in this table first before activating the google api for a translation.  The project has tables cached for the first 100k english words and their translations to the 14 languages above languages are stored, along with the translations of those phrases back to english.


## Python API

```python
# translate phrases to multiple languages
# defaults to popular languages (must have
# Google Translate API key to use)
class Babelfish:
    def addLangauge(langauge): pass # ex "English"
    def removeLanguage(language): pass
    def translate(words): pass
    # { 'en': 'phrase', 'es': 'phrase', etc. }

# As above, but uses/updates local sqlite
# database (only needs Google API key if used
# for uncached translation)
class CachedBabelfish: pass

class Phrase: pass # single phrase
class PhraseTable: pass # phrase table model
class Translate: pass # single translation
class TranslateTable: pass # translate table model
class Bad: pass # single bad word
class BadTable: pass # bad table model

# model for above tables.
class Db
  .translate
  .phrase
  .bad


```


language(text)|(con)

# Dev Notes
## Google Translate API Key

ID: brainwallet-1573921011875
Service account, starting-account-43t7oxohtak0

## Setup

https://cloud.google.com/translate/docs/basic/setup-basic

. .env

```bash
curl -s -X POST -H "Content-Type: application/json" \
    -H "Authorization: Bearer "$(gcloud auth application-default print-access-token) \
    --data "{
  'q': 'The Great Pyramid of Giza (also known as the Pyramid of Khufu or the
        Pyramid of Cheops) is the oldest and largest of the three pyramids in
        the Giza pyramid complex.',
  'source': 'en',
  'target': 'es',
  'format': 'text'
}" "https://translation.googleapis.com/language/translate/v2"
```

key is in lastpass note on brainwallet
```bash
conda create -n brainwallet python=3.7 python
conda activate brainwallet
```
or

```bash
cd <here>
python3 -m venv metabrainwallet
. metabrainwallet/bin/activate  # unix 
metabrainwallet/bin/activate.bat # windows
pip install --upgrade google-cloud-translate
pip install --upgrade python-dotenv
```
either way, you need a google api key

```bash
echo 'GOOGLE_APPLICATION_CREDENTIALS="${HOME}/projects/metabrainwallet/brainwallet-7e933180334f.json"' > .env
# save contents of brainwallet-7e933180334f.json from lastpass/brainwallet to brainwallet-7e933180334f.json
```

