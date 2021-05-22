#!/usr/bin/env bash

cd ../../ai

echo "Scraping data from AlphaVantage for $1 [last $2 days]"
echo "--------------------------------------------------------------"

python -m pipenv run python -m \
scraper \
-t $1 \
-d $2

echo "--------------------------------------------------------------"
echo "Done! Unless there was an error, the file will be saved @ data/$1.json"
