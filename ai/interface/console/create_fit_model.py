def create_fit_model(args):
    from actions import create_fit_model as cfm
    from entities.ETO import task_eto
    from datetime import datetime

    run = cfm.delay if args.delay else cfm

    task = run(
        ticker=args.ticker if args.ticker else Exception('Missing ticker symbol'),
        features=args.features.split(',') if args.features else ['Close'], 
        tech_features=args.tech_features.split(',') if args.tech_features else ['Open', 'High', 'Low', 'Volume', 'MACD', 'RSI', 'BBS'],
        sequence_size=int(args.sequence_size) if args.sequence_size else Exception('Missing sequence size'), 
        rolling_window=args.rolling_window if args.rolling_window else -1, 
        training_data_size=int(args.training_data_size) if args.training_data_size else 100, 
        output_sequence_size=int(args.output_sequence_size) if args.output_sequence_size else 1, 
        edge_layer_units=int(args.edge_layer_units) if args.edge_layer_units else Exception('Missing number of units in edge layers'), 
        layers=args.layers.split(',') if args.layers else [],
        batch_size=args.batch_size if args.batch_size else 1, 
        epochs=int(args.epochs) if args.epochs else Exception('Missing number of training epochs'), 
        input_dropout=float(args.input_dropout) if args.input_dropout else 0.0,
        recurrent_dropout=float(args.recurrent_dropout) if args.recurrent_dropout else 0.0,
        stateful=True if args.stateful is None else bool(args.stateful), 
        _data=args.data if args.data else Exception('Missing ohlcv time series data'), 
        _description=args.description if args.description else Exception('Missing model description')
    )

    return (task if not args.delay else task_eto(
        task.id,
        'create_fit_model',
        datetime.now().timestamp()
    ).__dict__)