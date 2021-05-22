#!/usr/bin/env bash

cd ../../ai

python -m pipenv run python -m \
console \
-a refit_model \
-mid $1 \
-e $3 \
-d data/$2.json
