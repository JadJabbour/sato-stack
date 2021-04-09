import os

# from invoke import run
from subprocess import Popen, DETACHED_PROCESS

from lib import io_manager

def ctrl_workers(action):
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

    # run("celery multi {action} {training_worker_name} {inference_worker_name} "\
    #       "-Q:{training_worker_name} {training_worker_name} -Q:{inference_worker_name} {inference_worker_name} "\
    #       "-c {concurrency} -l {logging} -A actions "\
    #       "--pidfile=celerydata/celery-pids/%n.pid --logfile=celerydata/celery-logs/%n.log".format(
    #           action=action, 
    #           training_worker_name=training_worker_queue, 
    #           inference_worker_name=inference_worker_queue,
    #           concurrency=concurrency,
    #           logging=logging
    #     )
    # )    
    
    return Popen("pipenv run celery -A actions worker -Q training -l debug -P solo".split(), creationflags=DETACHED_PROCESS)
