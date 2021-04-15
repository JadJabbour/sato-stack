#!/usr/bin/env bash

cd ../../ai

## Scrape ticker data

python -m pipenv run python -m scraper \
-t $1 \
-sd 2018-01-01 \
-ed 2021-04-15 
