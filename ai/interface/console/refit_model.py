def refit_model(args):
    from actions import refit_model as rfm
    return rfm(
        model_id=args.model_id if args.model_id else Exception('Missing model ID'),
        training_data_size=int(args.training_data_size) if args.training_data_size else 95, 
        epochs=int(args.epochs) if args.epochs else Exception('Missing number of training epochs'), 
        _data=args.data if args.data else Exception('Missing ohlcv time series data')
    )
