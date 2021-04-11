class zero_router(object):
    def create_fit_model(self, ticker, sequence_size, output_sequence_size, edge_layer_units, layers, epochs, data, description):
        from actions import create_fit_model as cfm
        from entities.ETO import task_eto
        from datetime import datetime

        task = cfm.delay(
            ticker= ticker if ticker else Exception('Missing ticker symbol'),
            features= ['Open', 'High', 'Low', 'Close'], 
            tech_features= ['MACD', 'RSI', 'BBS'], 
            sequence_size= sequence_size if sequence_size else Exception('Missing sequence size'), 
            rolling_window= -1, 
            training_data_size= 80, 
            output_sequence_size= int(output_sequence_size) if output_sequence_size else 1, 
            edge_layer_units= int(edge_layer_units) if edge_layer_units else Exception('Missing number of units in edge layers'), 
            layers= layers.split(',') if layers else Exception('Missing shape of hidden layers'),
            batch_size= 1, 
            epochs= int(epochs) if epochs else Exception('Missing number of training epochs'), 
            input_dropout= 0.1,
            recurrent_dropout= 0.1,
            stateful= True, 
            _data= data if data else Exception('Missing ohlcv time series data'), 
            _description= description if description else Exception('Missing model description')
        )
        
        return task_eto(
            task.id,
            'create_fit_model',
            datetime.now().timestamp()
        ).__dict__

    def refit_model(self, **kwargs):
        from actions import refit_model as rfm
        from entities.ETO import task_eto
        from datetime import datetime
        
        task = rfm.delay(
            model_id=kwargs.model_id if kwargs.model_id else Exception('Missing model ID'),
            training_data_size=int(kwargs.training_data_size) if kwargs.training_data_size else 95, 
            epochs=int(kwargs.epochs) if kwargs.epochs else Exception('Missing number of training epochs'), 
            _data=kwargs.data if kwargs.data else Exception('Missing ohlcv time series data')
        )

        return task_eto(
            task.id,
            'refit_model',
            datetime.now().timestamp()
        ).__dict__