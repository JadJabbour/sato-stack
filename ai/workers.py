import os

from subprocess import Popen, DETACHED_PROCESS

from lib import io_manager

def launch_workers(action):
    io = io_manager(do_init=False)

    io.load_config(config_file_path='config.ini')

    training_worker_queue, inference_worker_queue, broker, backend = io.load_celery_config()
    concurrency, logging = io.load_celery_worker_config()

    if(not os.path.isdir("celerydata")):
        os.mkdir("celerydata")
 
    if(not os.path.isdir("celerydata/celery-pids")):
        os.mkdir("celerydata/celery-pids")

    if(not os.path.isdir("celerydata/celery-logs")):
        os.mkdir("celerydata/celery-logs")

    cmd_training = "pipenv run celery -A actions worker -Q {training_worker_queue} -l {logging} -c {concurrency} -P solo --pidfile=celery-pids/training.pid --logfile=celery-logs/training.log".format(training_worker_queue, logging, concurrency)  
    cmd_inference = "pipenv run celery -A actions worker -Q {inference_worker_queue} -l {logging} -c {concurrency} -P solo --pidfile=celery-pids/inference.pid --logfile=celery-logs/inference.log".format(inference_worker_queue, logging, concurrency) 
    
    return [ 
        Popen(cmd_training.split(), creationflags=DETACHED_PROCESS),
        Popen(cmd_inference.split(), creationflags=DETACHED_PROCESS)
    ]
