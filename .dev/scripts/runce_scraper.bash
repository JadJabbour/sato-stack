#!/usr/bin/env bash

cd ../../ai

echo "Scraping data from AlphaVantage for $2 [last $3 days]"
echo "--------------------------------------------------------------"

python -m pipenv run python -m \
scraper \
-m $1 \
-t $2 \
-d $3

echo "--------------------------------------------------------------"
echo "Done! Unless there was an error, the file will be saved @ data/$2.json"
