import sys
import os

import pandas_datareader as pdr

from lib import io_manager

def scraper():
    try:
        args_def = [
            ('-t', '--ticker', 'The ticker symbol to retreive the data for', str),
            ('-sd', '--start_date', 'The start date of the dataset', str),
            ('-ed', '--end_date', 'The end date of the dataset', str)
        ]

        args = io_manager.parse_args("Seers.ai.scraper", "Scrapes ticker data and stores in ./data", args_def)

        series = pdr.DataReader(
            args.ticker, 
            data_source='yahoo', 
            start=args.start_date, 
            end=args.end_date
        )

        series = series[~series.index.duplicated(keep='last')]
        series.rename(columns={'Adj Close': 'Adj_Close'}, inplace=True)
        json = series.to_json(orient='index')
        
        if(not os.path.isdir("data")):
            os.mkdir("data")

        with open('/'.join(['data', '.'.join([args.ticker, 'json'])]), 'w') as f:
            f.write(json)

        return json
    except Exception as ex:
        print(str(ex))

if __name__ == "__main__":
    scraper()
    sys.exit()