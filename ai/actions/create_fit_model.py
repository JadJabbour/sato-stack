from actions.celery import clapp, training_worker_queue
import sys
@clapp.task(queue=training_worker_queue)
def create_fit_model(ticker, features, tech_features, rolling_window, training_data_size, sequence_size, output_sequence_size, edge_layer_units, layers, batch_size, epochs, input_dropout, recurrent_dropout, stateful, _data, _description):
    import math

    from lib import io_manager, data_manager, model_manager, db_manager
    from entities.domain import lstm_model

    io = io_manager()
    dpp = data_manager()
    mm = model_manager()

    io_manager.throw_if_except(ticker, sequence_size, edge_layer_units, layers, epochs, _data, _description)

    config = io.configuration
    session_id = io.session_id
    out_to = io.output
    
    io.load_logging()

    optimizer, loss = io.load_network_definition()
    scaling_name = io.load_data_scaling_type()
    plot_style, plot_title, plot_fig_size, plot_x_label, plot_y_label, output_file_name, output_dpi, figformat, show_plot = io.load_plot_definition()
    host, port, auth_source, user, pwd, dbname = io.load_db_config()
    
    dbconn = db_manager(
        host=host,
        port=port,
        auth_source=auth_source,
        user=user,
        pwd=pwd,
        dbname=dbname
    )

    df = dpp.data_unique_series(_data)

    all_features = features.copy()
    tech_feature_labels = []

    df_offset = 30 if rolling_window == -1 else rolling_window

    if len(tech_features) > 0:
        df = dpp.calculate_tech_features(df, rolling_window, tech_features)[df_offset:]
        for tft in tech_features:
            if tft == 'MACD':
                all_features.append('MACD')
                all_features.append('MACDSIG')
                tech_feature_labels.append('MACD')
                tech_feature_labels.append('MACDSIG')
            elif tft == 'BBS':
                all_features.append('BBL')
                all_features.append('BBU')
                all_features.append('BBM')
                tech_feature_labels.append('BBL')
                tech_feature_labels.append('BBU')
                tech_feature_labels.append('BBM')
            else:
                all_features.append(tft)
                tech_feature_labels.append(tft)

    df_rawdata = df.copy() 
    df = dpp.select_data_features(df, all_features)
    
    train_data, test_data, test_data_index_range, training_data_len = dpp.split_train_test_data(df, training_data_size, sequence_size, batch_size)

    scaled_train_data, scaled_test_data, scalers = dpp.scale_data_features(train_data, test_data, scaling_name, all_features)

    x_train, y_train, x_test, y_test = dpp.group_data_by_sequence_to_numpy(scaled_train_data, scaled_test_data, sequence_size, output_sequence_size, features, tech_feature_labels)

    lstm = mm.create_model(edge_layer_units, layers, optimizer, loss, len(features), (batch_size, x_train.shape[1], len(all_features)), output_sequence_size, input_dropout, recurrent_dropout, stateful)

    mm.visualize_network(out_to)

    fitres = mm.fit_model(x_train, y_train, batch_size, epochs)

    predictions, scaled_predictions = mm.generate_prediction(x_test, features, output_sequence_size, test_data_index_range, scalers, batch_size)

    display_from_original = df_rawdata['Close'][training_data_len-math.ceil(len(test_data_index_range)*1.5):]

    # to_disp = [display_from_original]
    # ci = 1
    # for pred in predictions:
    #     to_disp.append(pred['Close'])
    #     ci += 1



    display = []
    display.append(([display_from_original, predictions], ['Close', 'Predicted']))

    for td in display:
        io.plot_datasets(plot_style, ticker + ' Close ' + plot_title, td[0], plot_fig_size, plot_x_label, plot_y_label, ticker + '_Close', output_dpi, figformat, td[1], show_plot)

    pkl_model, pkl_scalers = mm.picklify()

    fixed_idx_pred = []
    for p in predictions:
        p.index = p.index.map(str)
        p = p.to_dict(orient='index')
        fixed_idx_pred.append(p)

    model = lstm_model(
        model_id=session_id,
        parameters={
            "ticker": ticker, 
            "features": features, 
            "tech_features": tech_features, 
            "rolling_window": rolling_window, 
            "training_data_size": training_data_size, 
            "sequence_size": sequence_size, 
            "output_sequence_size": output_sequence_size, 
            "edge_layer_units": edge_layer_units, 
            "layers": layers, 
            "batch_size": batch_size, 
            "epochs": epochs, 
            "input_dropout": input_dropout, 
            "recurrent_dropout": recurrent_dropout, 
            "stateful": stateful
        },
        training_data_length=training_data_len,
        features=all_features,
        score=str(fitres),
        test_predictions=fixed_idx_pred,
        model=pkl_model,
        description=_description,
        scalers=pkl_scalers,
        refits=[]
    )

    dbconn.connectdb()

    model.save()

    dbconn.disconnectdb()

    return io.session_id, rmse