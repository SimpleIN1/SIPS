from __future__ import annotations

import pickle
import logging
from CeleryApp.app import app
from django.core.mail.message import EmailMultiAlternatives


@app.task
def send_email_with_broker(notification_pickle) -> None:
    notification: EmailMultiAlternatives = pickle.loads(notification_pickle)
    logging.info(f'|||->send mail to {notification.to}<-|||')
    notification.send()
    logging.info('|||->sending mail is success<-|||')
