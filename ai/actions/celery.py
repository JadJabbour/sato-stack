from lib import io_manager, celery_manager

io = io_manager(do_init=False)
io.load_config(config_file_path='config.ini')

training_worker_queue, inference_worker_queue, broker, backend = io.load_celery_config()

clapp = celery_manager(app_name='actions', broker=broker, backend=backend, include=['actions.create_fit_model', 'actions.refit_model', 'actions.generate_prediction'])

if __name__ == "__main__":
    clapp.start()