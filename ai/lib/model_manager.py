import math
import datetime

import numpy as np
import pandas as pd

from pickle import dumps as pdumps, loads as ploads

from tensorflow import keras as kr
from tensorflow.keras import utils as keras_utils
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, LSTM, Dropout, deserialize, serialize
from tensorflow.python.keras.saving import saving_utils

class model_manager(object):
    def __init__(self, modelpkl=None, scalerpkls=None):
        ## this where device detection, devices state loading and device selectrion should occur on multi-gpu
        self.model, self.scalers = None, None
        if modelpkl is not None and scalerpkls is not None:
            self.load_model(modelpkl, scalerpkls)

    def load_model(self, modelpkl, scalerpkls):
        model_manager.keras_picklable_wrapper(Model)

        self.model = ploads(modelpkl)
        self.scalers = {}

        for key in scalerpkls.keys():
            self.scalers[key] = ploads(scalerpkls[key])

        return self.model, self.scalers

    def create_model(self, edge_layers_units, layers, optimizer, loss, output_features, training_data_shape, input_do=0., recurr_do=0., stateful=True):
        model_manager.keras_picklable_wrapper(Model)

        model = Sequential()
        model.add(LSTM(int(edge_layers_units), return_sequences=True, batch_input_shape=training_data_shape, stateful=stateful))

        if input_do > 0:
            model.add(Dropout(input_do))

        for j in range(len(layers)):
            model.add(LSTM(int(layers[j]), return_sequences=True, stateful=stateful))    
            if recurr_do > 0:
                model.add(Dropout(recurr_do))

        model.add(LSTM(int(edge_layers_units), return_sequences=False, stateful=stateful))
        if recurr_do > 0:
            model.add(Dropout(recurr_do))

        model.add(Dense(math.floor(int(edge_layers_units)/2)))
        model.add(Dense(output_features))
        model.compile(optimizer=optimizer, loss=loss)

        self.model = model

        return self.model

    def fit_model(self, x_data, y_data, batch_size, epochs):
        self.model.fit(x_data, y_data, batch_size=int(batch_size), epochs=int(epochs))
        return self.model

    def inverse_scale(scaler, data):
        return scaler.inverse_transform(data)

    def generate_prediction(self, x_data, features, df_indeces=None, scalers=None, batch_size=1):
        sclrs = scalers if scalers is not None else self.scalers

        scaled_predictions = self.model.predict(x_data, batch_size)
        predictions = pd.DataFrame(data=scaled_predictions, index=df_indeces, columns=features)

        for feat in features:
            predictions[feat] = model_manager.inverse_scale(sclrs[feat], predictions[[feat]])

        self.scalers = sclrs
        return predictions, scaled_predictions

    def visualize_network(self, output):
        keras_utils.plot_model(self.model, to_file="/".join([output,"model_map.png"]), show_shapes=True)

    def evaluate_model(scaled_predictions, valid): 
        return np.sqrt(np.mean(scaled_predictions-valid)**2)        

    def picklify(self):
        pkl_mdl = pdumps(self.model)

        pkl_sclr = {}
        for key in self.scalers.keys():
            pkl_sclr[key] = pdumps(self.scalers[key])

        return pkl_mdl, pkl_sclr

    def unpack_pickled_model(model, training_config, weights):
        restored_model = deserialize(model)
        if training_config is not None:
            restored_model.compile(
                **saving_utils.compile_args_from_training_config(
                    training_config
                )
            )
        restored_model.set_weights(weights)
        return restored_model


    def keras_picklable_wrapper(cls):
        def __reduce__(self):
            model_metadata = saving_utils.model_metadata(self)
            training_config = model_metadata.get("training_config", None)
            model = serialize(self)
            weights = self.get_weights()
            return (cls.seersai_upack, (model, training_config, weights))
            
        cls.__reduce__ = __reduce__
        cls.seersai_upack = model_manager.unpack_pickled_model
