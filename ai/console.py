import sys

from json_tricks import dumps

import interface
from lib import io_manager
##  should add try catch to actions and raise proper exceptions
def run():
    args_def = [
        ('-a', '--action', 'The Seers.ai.actions to run', str),
        ('-mid', '--model_id', 'The Seers.ai.lstm_model`s id', str),
        ('-desc', '--description', 'A description of the model being created and fit', str),
        ('-t', '--ticker', 'The ticker/symbol managing model for', str),
        ('-sd', '--start_date', 'The start date for the time series forcasting', str),
        ('-ed', '--end_date', 'The end date for the time series forcasting', str),
        ('-f', '--features', 'The basic feature list', str),
        ('-tf', '--tech_features', 'The list of tech features to calculate and append to dataset', str),
        ('-rw', '--rolling_window', 'The size of the rolling window to use when calculating technical features, uses defaults when set to -1', int),
        ('-tz', '--training_data_size', 'The size of the training dataset (in percentages of original dataset size)', int), 
        ('-sz', '--sequence_size', 'The size of the sequence of data to be grouped together', int),
        ('-oz', '--output_sequence_size', 'The size of the sequence of ouput data(ie: the number of days to predict forward from each sequence from the time series)', int),
        ('-elu', '--edge_layer_units', 'The number of neurons on the outlying layers', int),
        ('-l', '--layers', 'A tuple of integers representing the shape of the inner layers', str),
        ('-ido', '--input_dropout', 'A decimal representing the dropout rate of the input layer in the network (to manage overfitting)', float),
        ('-rdo', '--recurrent_dropout', 'A decimal representing the recurrent dropout rate on subsequent layers in the network (to manage overfitting)', float),
        ('-st', '--stateful', 'Bit indicating whether the LSTM layers should be stateful (remembering previous batches)', int),
        ('-bz', '--batch_size', 'The size of the batches to group the data based on (defaults to 1, use in tandem with sequence_size) for optimal results', int),
        ('-e', '--epochs', 'The number of epochs/episodes of fitting model to data', int),
        ('-d', '--data', 'The json representation of the ohlcv time series dataset for training as string or filepath', str),
    ]

    args = io_manager.parse_args('Seers.ai.console', 'Console interface for Seers.ai', args_def)

    if args.action is not None and not args.action == "": 
        io_manager.out(
            dumps(
                getattr(interface.console, args.action)(args)
            ), 
            logger=None
        )
    else:
        raise Exception("No action was specified")

if __name__ == "__main__":
    try:
        run()
    except Exception as ex:
        io_manager.out(ex, is_exception=True, exception_info=sys.exc_info(), logger=None)
    
    sys.exit()