def celery_manager(app_name, broker, **kwargs):
    from celery import Celery
    return Celery(app_name, broker=broker, **kwargs)