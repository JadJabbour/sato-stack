def create_fit_model(args):
    from actions import create_fit_model as cfm
    return cfm(
        ticker=args.ticker if args.ticker else Exception('Missing ticker symbol'),
        features=args.features.split(',') if args.features else ['Open', 'High', 'Low', 'Close'], 
        tech_features=args.tech_features.split(',') if args.tech_features else ['MACD', 'RSI', 'BBS'], 
        sequence_size=int(args.sequence_size) if args.sequence_size else Exception('Missing sequence size'), 
        rolling_window=args.rolling_window if args.rolling_window else -1, 
        training_data_size=int(args.training_data_size) if args.training_data_size else 80, 
        output_sequence_size=int(args.output_sequence_size) if args.output_sequence_size else 1, 
        edge_layer_units=int(args.edge_layer_units) if args.edge_layer_units else Exception('Missing number of units in edge layers'), 
        layers=args.layers.split(',') if args.layers else Exception('Missing shape of hidden layers'),
        batch_size=args.batch_size if args.batch_size else 1, 
        epochs=int(args.epochs) if args.epochs else Exception('Missing number of training epochs'), 
        input_dropout=float(args.input_dropout) if args.input_dropout else 0.1,
        recurrent_dropout=float(args.recurrent_dropout) if args.recurrent_dropout else 0.1,
        stateful=True if args.stateful is None else bool(args.stateful), 
        _data=args.data if args.data else Exception('Missing ohlcv time series data'), 
        _description=args.description if args.description else Exception('Missing model description')
    )