import math
import sys
import pandas as pd
import numpy as np

from json_tricks import dumps, loads
from finta import TA

from entities.constants import ohlcv_namemap
from entities.constants import scaler_map as sclr_map

class data_manager(object):
    def __init__(self, scaler_map=None, ohlcv_colmap=None):
        self.scaler_map = scaler_map if scaler_map is not None else sclr_map()
        self.ohlcv_map = ohlcv_colmap if ohlcv_colmap is not None else ohlcv_namemap()

    def load_json(self, json_str):
        return loads(json_str)

    def dump_json(self, data_obj):
        return dumps(data_obj)

    def data_unique_series(self, json, orient='index', convert_dates=True): 
        series = pd.read_json(
            path_or_buf = json,
            orient = orient,
            convert_dates = convert_dates
        )

        return series[~series.index.duplicated(keep='last')] 

    def select_data_features(self, df, features):
        return df.filter(features)

    def merge_dataframes(df1, df2, axis=1):
        return pd.concat([df1, df2], axis=axis)

    def floor_pos_int_or_min_default(integer, min_default):
        i = math.floor(integer)
        
        if i < 1 or i < min_default:
            return min_default

        return i

    def floor_pos_int_or_default(integer, default):
        i = math.floor(integer)

        if i < 1:
            return default

        return i
    
    def calculate_tech_features(self, df, rolling_window, tech_features_labels):
        tmp_df = df.copy()
        ret_df = df.copy()
        tmp_df.columns = tmp_df.columns.str.lower()

        if 'RSI' in tech_features_labels:
            ret_df['RSI'] = TA.RSI(tmp_df, period=data_manager.floor_pos_int_or_default(rolling_window,14)).to_numpy()

        if 'EVWMA' in tech_features_labels:
            ret_df['EVWMA'] = TA.EVWMA(tmp_df, period=data_manager.floor_pos_int_or_default(rolling_window,20))

        if 'MACD' in tech_features_labels:
            macd = TA.MACD(
                tmp_df,
                period_fast=data_manager.floor_pos_int_or_default(rolling_window/2,12),
                period_slow=data_manager.floor_pos_int_or_default(rolling_window,26),
                signal=data_manager.floor_pos_int_or_default(rolling_window/3,9)
            )
            ret_df['MACD'] = macd.iloc[:,0].to_numpy()
            ret_df['MACDSIG'] = macd.iloc[:,1].to_numpy()

        if 'BBS' in tech_features_labels:
            bbs = TA.BBANDS(
                tmp_df, 
                period=data_manager.floor_pos_int_or_default(rolling_window,20), 
                MA=TA.KAMA(
                    tmp_df, 
                    period=data_manager.floor_pos_int_or_default(rolling_window,20), 
                    er=data_manager.floor_pos_int_or_default(rolling_window/2,10), 
                    ema_fast=data_manager.floor_pos_int_or_min_default(rolling_window/10,2), 
                    ema_slow=data_manager.floor_pos_int_or_default(rolling_window+10,30)
                )
            )
            ret_df['BBU'] = bbs.iloc[:,0].to_numpy()
            ret_df['BBM'] = bbs.iloc[:,1].to_numpy()
            ret_df['BBL'] = bbs.iloc[:,2].to_numpy()

        return ret_df

    def shift_add_recalc_tech_feats(self, original_df, new_df, rolling_window, tech_features_labels, shift_by=1):
        # need to find a way to recalculate for only the new df
        ret_df = data_manager.merge_dataframes(original_df, new_df)[-shift_by:]
        return self.calculate_tech_features(ret_df, rolling_window, tech_features_labels)

    def split_train_test_data(self, df, split_rate, sequence_size, batch_size):
        training_data_len = math.ceil(len(df)*(split_rate/100)) if split_rate < 100 else len(df)

        train_data = df.iloc[0:training_data_len,:].copy()
        test_data = df.iloc[training_data_len:,:].copy() if split_rate < 100 else df.iloc[math.ceil(len(df)*0.8):,:].copy()

        to_drop_train = len(train_data)%batch_size
        to_drop_test = len(test_data)%batch_size
        
        if to_drop_train > 0:
            train_data = train_data[to_drop_train:]

        if to_drop_test > 0:
            test_data = test_data[:-1 * to_drop_test]

        test_data_index_range = test_data.index[sequence_size:]

        return train_data, test_data, test_data_index_range, training_data_len
    
    def scale_feature(train_data, test_data, scaler_type, feature_range=(0,1)):
        active_scaler = scaler_type(feature_range=feature_range).fit(train_data)
        return active_scaler.transform(train_data), active_scaler.transform(test_data), active_scaler

    def scale_data_features(self, train_data, test_data, scaler_type, features, pickled_scalers=None, feature_range=(0,1)):
        td, tx = train_data.copy(), test_data.copy()
        scalers = {}

        for f in features:
            if(pickled_scalers is not None):
                td[f], tx[f], scalers[f] = pickled_scalers[f].transform(td[[f]]), pickled_scalers[f].transform(tx[[f]]), pickled_scalers[f]
            else:
                td[f], tx[f], scalers[f] = data_manager.scale_feature(td[[f]], tx[[f]], self.scaler_map[scaler_type], feature_range)

        return td, tx, scalers

    def scale_data_for_inference(self, x_data, features, scalers):
        xd = x_data.copy()

        for f in features:
            xd[f] = scalers[f].transform(xd[[f]])

        return xd

    def group_data_by_sequence_to_numpy(self, train_data, test_data, sequence_size, output_seq_size, features, tech_features):
        x_train, y_train, x_test, y_test = [], [], [], []
        train_data = train_data.values
        test_data = test_data.values
        features_idx = []
        features_idx_dict = {
            'Open': 0,
            'High': 1,
            'Low': 2,
            'Close': 3
        }

        for f in features:
            features_idx.append(features_idx_dict[f])

        for i in range(sequence_size, (len(train_data)-(output_seq_size-1))):
            x_train.append(train_data[i-sequence_size:i,:])
            y_train.append(train_data[i:i+output_seq_size,features_idx])
        
        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], len(features)+len(tech_features))) 
        y_train = np.reshape(y_train, (y_train.shape[0], y_train.shape[1], len(features))) 

        for i in range(sequence_size, (len(test_data)-(output_seq_size-1))):
            x_test.append(test_data[i-sequence_size:i,:])
            y_test.append(test_data[i:i+output_seq_size,features_idx])

        x_test, y_test = np.array(x_test), np.array(y_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], len(features)+len(tech_features)))
        y_test = np.reshape(y_test, (y_test.shape[0], y_test.shape[1], len(features))) 

        return x_train, y_train, x_test, y_test
        
    def sequence_to_numpy_for_inference(self, data, sequence_size, features, tech_features):
        x_data = []
        data = data.values

        if(sequence_size == len(data)):
            x_data.append(data[:,:])
        else:
            for i in range(sequence_size, len(data)):
                x_data.append(data[i-sequence_size:i,:])

        x_data = np.array(x_data)

        x_data = np.reshape(x_data, (x_data.shape[0], x_data.shape[1], len(features)+len(tech_features)))

        return x_data
