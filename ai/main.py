import sys
from lib import db_manager
from entities.domain import lstm_model

dbconn = db_manager(
    host="127.0.0.1",
    port=27017,
    auth_source="admin",
    user="localadmin",
    pwd="Ysg52_sKia",
    dbname="seersaistore"
)

dbconn.connectdb()

model = lstm_model(
    model_id="12345",
    parameters={'key': 'value'},
    training_data_length=1000,
    features=['f1','f2'],
    model="binary data as string",
    description="",
    scalers="binary data as string"
)

model.save()

dbconn.disconnectdb()

print('success, check db')