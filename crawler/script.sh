#! /usr/bin/bash

pip3 install BeautifulSoup4

DATASET_URL='http://www.cim.mcgill.ca/~dudek/206/Logs/AOL-user-ct-collection/user-ct-test-collection-06.txt.gz'
DATASET_PATH='./dataset.txt'

wget $DATASET_URL -O $DATASET_PATH.gz && gunzip $DATASET_PATH.gz

python3 crawler.py

rm 'dataset.txt'