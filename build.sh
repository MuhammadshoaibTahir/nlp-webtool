#!/usr/bin/env bash
pip install -r requirements.txt
python -m textblob.download_corpora
gunicorn app:app --timeout 90