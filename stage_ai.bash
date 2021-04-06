#!/usr/bin/env bash

cd ai && \

## Staging fresh model and fitting

python -m pipenv run python -m console \
-a create_fit_model \
-desc 'a model for predicting trx-usd price fluctuations' \
-t TRX-USD \
-sz 8 -oz 1 \
-elu 64 -l 32,32 \
-e 1 \
-d data/trx.json


## Staging model loading and reffitting

# python -m pipenv run python -m console \
# -a refit_model \
# -mid 4fe3140991d911eb8ec58c6ded4ce976 \
# -e 20 \
# -d data/trx.json


## Staging fresh model and fitting

# cd ai && python -m pipenv run python -m console \
# -a generate_predictions