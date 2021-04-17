#!/usr/bin/env bash

## Scraping data 

bash ./runce_scraper.bash $1
tick="Model for predicting ${1} fluctuations"

## Staging fresh model and fitting

cd ../../ai

python -m pipenv run python -m console -a create_fit_model \
-desc "${tick}" \
-t $1 \
-ido 0.1 -rdo 0.1 \
-tz 90 \
-sz 7 -oz 2 -elu 72 -l 144 -e 36 \
-d data/$1.json
