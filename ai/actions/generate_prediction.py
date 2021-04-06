from lib import io_manager, data_manager, model_manager
from jobs import tasker as cltsk

tasker = cltsk()

@tasker.inference.task
def generate_prediction():
    raise NotImplementedError()