#!/bin/sh

set -e

pip3 install -r requirements.txt

cat data/news_ru.jsonl | python3 main.py >> news_ru_labeled.jsonl

