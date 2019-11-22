# Brainwallet

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
conda create -n brainwallet python=3.7 python
conda activate brainwallet

or

cd <here>
python3 -m venv metabrainwallet
metabrainwallet/bin/activate  # or, in windows: metabrainwallet/bin/activate.bat
pip install --upgrade google-cloud-translate
pip install --upgrade python-dotenv
echo 'GOOGLE_APPLICATION_CREDENTIALS="${HOME}/projects/metabrainwallet/brainwallet-7e933180334f.json"' > .env
# save contents of brainwallet-7e933180334f.json from lastpass/brainwallet to brainwallet-7e933180334f.json


