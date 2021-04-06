import math
import datetime

from lib import io_manager, data_manager, model_manager, db_manager
from entities.domain import lstm_model
from jobs import tasker as cltsk

tasker = cltsk()

@tasker.training.task
def refit_model(model_id, training_data_size, epochs, _data):
    io = io_manager(session_id=model_id)
    dpp = data_manager()

    io_manager.throw_if_except(model_id, epochs, _data)

    config = io.configuration
    session_id = io.session_id
    out_to = io.output
    logger = io.load_logging()

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

    dbconn.connectdb()

    model_rec = lstm_model.objects.get(model_id=model_id)

    dbconn.disconnectdb()

    mm = model_manager(model_rec.model, model_rec.scalers)

    model = mm.model
    pre_scalers = mm.scalers
    ticker = model_rec.parameters['ticker']
    features = model_rec.parameters['features']
    tech_features = model_rec.parameters['tech_features']
    rolling_window = model_rec.parameters['rolling_window'] 
    sequence_size = model_rec.parameters['sequence_size'] 
    output_sequence_size = model_rec.parameters['output_sequence_size'] 
    batch_size = model_rec.parameters['batch_size'] 

    df = dpp.data_unique_series(_data)

    all_features = features.copy()
    tech_feature_labels = []

    df_offset = 30 if rolling_window == -1 else rolling_window

    if len(tech_features) > 0:
        df = dpp.calculate_tech_features(df, rolling_window, tech_features)[df_offset:]
        for tft in tech_features:
            if tft == 'MACD':
                all_features.append(tft)
                all_features.append('MACDSIG')
                tech_feature_labels.append(tft)
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

    scaled_train_data, scaled_test_data, scalers = dpp.scale_data_features(train_data, test_data, scaling_name, all_features, pre_scalers)

    x_train, y_train, x_test, y_test = dpp.group_data_by_sequence_to_numpy(scaled_train_data, scaled_test_data, sequence_size, output_sequence_size, features, tech_feature_labels)
    
    model = mm.fit_model(x_train, y_train, batch_size, epochs)

    predictions, scaled_predictions = mm.generate_prediction(x_test, features, test_data_index_range, pre_scalers, batch_size)

    rmse = model_manager.evaluate_model(scaled_predictions, y_test)

    display_from_original = df_rawdata['Close'][training_data_len-math.ceil(len(test_data_index_range)*1.5):]

    display = []
    display.append(([display_from_original, predictions['Close']], ['Close', 'P_'+'Close']))

    for td in display:
        io.plot_datasets(plot_style, ticker + ' Close ' + plot_title, td[0], plot_fig_size, plot_x_label, plot_y_label, ticker + '_Close', output_dpi, figformat, td[1], show_plot)

    pkl_model, pkl_scalers = mm.picklify()

    model_rec.model = pkl_model
    model_rec.scalers = pkl_scalers
    model_rec.updated_at = datetime.datetime.utcnow()

    model_rec.refits = model_rec.refits.append({
        'refited_at': datetime.datetime.utcnow(),
        'rmse': rmse,
        'test_predictions': predictions.to_dict(orient='index')
    })

    dbconn.connectdb()

    model_rec.save()

    dbconn.disconnectdb()

    return io.session_id, rmse