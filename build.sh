#!/usr/bin/env bash
pip install --upgrade pip
pip install -r requirements.txt
python -m nltk.downloader punkt
python -m textblob.download_corpora
python -m spacy validate