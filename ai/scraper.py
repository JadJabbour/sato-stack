import sys
import os

import json

from urllib import request
import pandas as pd

from lib import io_manager, data_manager

def scraper():
    try:
        dpp = data_manager()

        args_def = [
            ('-m', '--market', 'The market to get data from', str),
            ('-t', '--ticker', 'The ticker symbol to retreive the data for', str),
            ('-d', '--days', 'The number of days of historical data to keep', int)
        ]

        args = io_manager.parse_args("Seers.ai.scraper", "Scrapes ticker data and stores in ./data", args_def)

        url=""
        idx=""
        base = "https://www.alphavantage.co/query?function={}&market=USD&apikey=0GXJV8P6GG8E9347&symbol={}&outputsize=full"
        if(args.market == 'crypto'):
            url="DIGITAL_CURRENCY_DAILY"
            idx='Time Series (Digital Currency Daily)'
            o='1a. open (USD)'
            h='2a. high (USD)'
            l='3a. low (USD)'
            c='4a. close (USD)'
        else:
            url="TIME_SERIES_DAILY"
            idx='Time Series (Daily)'
            o='1. open'
            h='2. high'
            l='3. low'
            c='4. close'
        
        response = request.urlopen(base.format(url, args.ticker))

        data = dpp.data_unique_series(json.dumps(json.load(response)[idx]))

        if(len(data) > args.days):
            data = data.iloc[0:args.days,:]

        data.rename(columns={
            o: dpp.ohlcv_map.open_col,
            h: dpp.ohlcv_map.high_col,
            l: dpp.ohlcv_map.low_col,
            c: dpp.ohlcv_map.close_col,
            '5. volume': dpp.ohlcv_map.vol_col,
        }, inplace=True)

        data = dpp.select_data_features(data, [
            dpp.ohlcv_map.open_col,
            dpp.ohlcv_map.high_col,
            dpp.ohlcv_map.low_col,
            dpp.ohlcv_map.close_col,
            dpp.ohlcv_map.vol_col,
        ])

        data.sort_index(inplace=True)

        print("\nPulled {} records for {}\n".format(str(len(data)), args.ticker))

        json_data = data.to_json(orient='index')
        
        if(not os.path.isdir("data")):
            os.mkdir("data")

        with open('/'.join(['data', '.'.join([args.ticker, 'json'])]), 'w') as f:
            f.write(json_data)

        return json_data
    except Exception as ex:
        print("\nError", ex, "\n")

if __name__ == "__main__":
    scraper()
    sys.exit()