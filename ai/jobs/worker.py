import os

import subprocess

from lib import io_manager

def worker():    
    io = io_manager(do_init=False)

    io.load_config(config_file_path='config.ini')

    training_worker, inference_worker, training_worker_name, inference_worker_name, broker, command, working_dir, daemonize = io.load_celery_config()

    os.chdir(working_dir)

    cmd_trainer = command.replace('__app_name__', training_worker_name).replace('__broker__', broker)
    cmd_inferer = command.replace('__app_name__', inference_worker_name).replace('__broker__', broker)

    if daemonize :
        cmd_trainer = " ".join([cmd_trainer, "-D"])
        cmd_inferer = " ".join([cmd_inferer, "-D"])

    return [
        subprocess.Popen(cmd_trainer) if training_worker else None,
        subprocess.Popen(cmd_inferer) if inference_worker else None,
    ]