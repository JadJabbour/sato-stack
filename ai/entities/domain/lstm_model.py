import datetime

from mongoengine import Document, StringField, DateTimeField, IntField, ListField, DictField, BinaryField, FloatField

class lstm_model(Document):
    model_id = StringField(required=True, primary_key=True)
    parameters = DictField(required=True)
    training_data_length = IntField(required=True)
    features = ListField(StringField(), required=True)
    rmse = FloatField(required=True)
    test_predictions = DictField(required=True)
    model = BinaryField(required=True)
    scalers = DictField(BinaryField(), required=True)
    description = StringField(required=True)
    refits = ListField(DictField())
    updated_at = DateTimeField(default=datetime.datetime.utcnow)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    meta = {'indexes': ['description', '$description', 'rmse']}
