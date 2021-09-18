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
--layers 75,75 \
--batch_size 1 \
--epochs 60 \
--data data/$1.json

# python -m pipenv run python -m console \
# --action create_fit_model \
# --description "${tick} :: stateful" -t $1 \
# --input_dropout 0.0 \
# --recurrent_dropout 0.4 \
# --stateful 1 \
# --sequence_size 16 \
# --output_sequence_size 1 \
# --edge_layer_units 64 \
# --batch_size 1 \
# --epochs 32 \
# --data data/$1.json

# --layers 128 \

## to try:
## one scaler for all
## including volume
## 
