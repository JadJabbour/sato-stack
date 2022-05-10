#!/usr/bin/env bash

tick="Model for predicting ${1}-USD price fluctuations"

cd ../../ai

python -m pipenv run python -m console \
--action create_fit_model \
--description "${tick}" -t $1 \
--input_dropout 0.1 \
--recurrent_dropout 0.1 \
--stateful 1 \
--sequence_size 60 \
--output_sequence_size 1 \
--edge_layer_units 50 \
--layers 75,150,75 \
--batch_size 1 \
--epochs 50 \
--data data/$1.json
