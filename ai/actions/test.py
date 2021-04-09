from actions.celery import clapp, training_worker_queue

@clapp.task(queue=training_worker_queue)
def test():
    import os

    os.mkdir('madeithere')

    return "im on redis"