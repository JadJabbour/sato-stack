from actions.celery import clapp, inference_worker_queue

@clapp.task(queue=inference_worker_queue)
def generate_prediction():
    from lib import io_manager, data_manager, model_manager
    raise NotImplementedError()