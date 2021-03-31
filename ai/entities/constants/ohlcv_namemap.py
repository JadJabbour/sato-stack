class ohlcv_namemap_builder(object):
    def __init__(self, o=None, h=None, l=None, c=None, a=None, v=None):
        self.open_col = 'Open' if o is None else o
        self.high_col = 'High' if h is None else h
        self.low_col = 'Low' if l is None else l
        self.close_col = 'Close' if c is None else c
        self.adj_close_col = 'AdjClose' if a is None else a 
        self.vol_col = 'Volume' if v is None else v

def ohlcv_namemap(config=None):
    return ohlcv_namemap_builder(
        o = config['open'],
        h = config['high'],
        l = config['low'],
        c = config['close'],
        a = config['adjclose'],
        v = config['volume']
    ) if config is not None else ohlcv_namemap_builder()