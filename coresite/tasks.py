from Anima.celery import app
from celery import shared_task


@shared_task
def add(x, y):
    return x + y


app.conf.beat_schedule = {
    'add-every-10-seconds': {
        'task': 'coresite.tasks.add',
        'schedule': 10.0,
        'args': (16, 16)
    },
}
