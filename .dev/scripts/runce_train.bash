#!/usr/bin/env bash

cd ../../ai

## Staging fresh model and fitting

python -m pipenv run python -m console -a create_fit_model \
-desc 'a model for predicting XRP-USD fluctuations' \
-t XRP-USD \
-ido 0.2 -rdo 0.3 \
-sz 30 -oz 1 -elu 80 -l 120 -e 50 \
-d data/XRP-USD.json
