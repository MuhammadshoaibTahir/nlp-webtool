#!/bin/bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
apt-get update && apt-get install -y python3-distutils
