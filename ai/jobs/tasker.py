from lib import io_manager, celery_manager

class tasker:
    def __init__(self, include):
        io = io_manager(do_init=False)
        io.load_config(config_file_path='config.ini')

        training_worker, inference_worker, training_worker_name, inference_worker_name, broker, command, working_dir, daemonize = io.load_celery_config()

        self.clapp = celery_manager(app_name='ai', broker=broker, include=include)