#!/usr/bin/env bash

## Scraping data 

bash ./runce_scraper.bash $1

## Staging fresh model and fitting

cd ../../ai

python -m pipenv run python -m console -a create_fit_model \
-desc 'a model for predicting $1 fluctuations' \
-t $1 \
-ido 0.0 -rdo 0.0 \
-tz 80 \
-sz 11 -oz 1 -elu 32 -l 128,64 -e 1 \
-d data/$1.json
