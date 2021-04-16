#!/usr/bin/env bash

cd ../../ai

### Scrape ticker data

## from date
printf -v from '2019-01-01' -1

## to today
printf -v date '%(%Y-%m-%d)T' -1 

echo "Scraping data from Yahoo for $1 [$from > $date]"
echo "--------------------------------------------------------------"

python -m pipenv run python -m scraper \
-t $1 \
-sd $from \
-ed $date 

echo "--------------------------------------------------------------"
echo "Done! Saved @ data/$1.json"