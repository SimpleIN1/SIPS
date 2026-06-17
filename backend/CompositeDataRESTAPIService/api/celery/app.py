import os

from celery import Celery, Task
from flask import Flask

import api.conf as conf
from api.common.email import init_mail
from api.db.base import db


# Init celery app
def celery_init_app(app: Flask):

    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask, broker=conf.broker_url, backend=conf.result_backend)
    celery_app.config_from_object('api.conf')
    celery_app.set_default()

    init_mail(app)

    app.extensions['celery'] = celery_app

    celery_app.conf.beat_schedule = {
        'Clear-user-access-token': {
            'task': 'api.celery.tasks.remove_expired_urls',
            'schedule': conf.TIMES_SCHEDULE['TIME_REMOVE_EXPIRED_URLS'],
        },
    }

    return celery_app


app = Flask(__name__, template_folder="../templates")

app.config.from_object('api.conf')
db.init_app(app)
celery_app = celery_init_app(app)

