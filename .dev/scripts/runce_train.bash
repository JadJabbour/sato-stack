#!/usr/bin/env bash

cd ../../ai

## Staging fresh model and fitting

python -m pipenv run python -m console -a create_fit_model \
-desc 'a model for predicting XRP-USD fluctuations' \
-t ETH-USD \
-ido 0.1 -rdo 0.2 \
-tz 97 \
-sz 16 -oz 1 -elu 32 -l 64,128 -e 100 \
-d data/ETH-USD.json
