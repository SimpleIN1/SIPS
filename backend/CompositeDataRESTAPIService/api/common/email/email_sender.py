import logging

from flask_mail import Message
from flask import render_template

from api import conf
from api.common.email import mail


class BaseEmail:
    subject = None
    template = None
    attrs = None

    def send_message(self, **kwargs):
        with mail.connect() as conn:
            sender = conf.MAIL_USERNAME
            if set(self.attrs).difference(set(kwargs.keys())):
                raise Exception(f"Incorrect attrs {self.attrs}")

            msg = Message(recipients=[kwargs["recipient"]],
                          subject=self.subject,
                          sender=sender)

            msg.html = render_template(self.template, name_service=conf.NAME, **kwargs)
            conn.send(msg)
            logging.info(f"Mail message is sent to {kwargs['recipient']}")


class SendLinksEmail(BaseEmail):
    subject = f"Ссылки для скачивания tiff-изображений — {conf.NAME}"
    template = "email/send_links.html"
    attrs = ("recipient", "links", "link_names")

