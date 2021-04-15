#!/usr/bin/env bash

cd ../../ai

## Staging model loading and reffitting

python -m pipenv run python -m console \
-a refit_model \
-mid 4fe3140991d911eb8ec58c6ded4ce976 \
-e 20 \
-d data/trx.json
