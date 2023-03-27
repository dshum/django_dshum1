from email.mime.image import MIMEImage
from email.mime.image import MIMEImage
from functools import lru_cache
from typing import Any, Optional, NamedTuple

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def convert_address(address: tuple | list[tuple] = None):
    if address is None:
        return None
    addresses = address if isinstance(address, list) else [address]
    return [f"{name} <{email}>" if name else email for (name, email) in addresses]


def get_common_scope():
    return {'site_name': settings.BASE_URL}


@lru_cache()
def attach_data(path: str, content_id: str):
    with open(finders.find(path), 'rb') as f:
        file_data = f.read()
    file = MIMEImage(file_data)
    file.add_header('Content-ID', content_id)
    return file


class Mailable:
    def __init__(self,
                 subject: str,
                 to: tuple | list[tuple],
                 template: str,
                 scope: dict[str: Any],
                 bcc: tuple | list[tuple] = None,
                 cc: tuple | list[tuple] = None,
                 from_email: tuple = None,
                 reply_to: str = None,
                 headers: dict[str: str] = None):
        scope.update(get_common_scope())

        self.subject = subject
        self.from_email = convert_address(from_email)
        self.to = convert_address(to)
        self.body = render_to_string(template, scope)
        self.cc = convert_address(cc)
        self.bcc = convert_address(bcc)
        self.reply_to = reply_to
        self.headers = headers

    def get_dict(self):
        return self.__dict__


class Mailer:
    def __init__(self, mailable: Mailable, connection=None):
        self.mailable = mailable
        params = self.mailable.get_dict()
        if connection:
            params.connection = connection
        self.message = EmailMessage(**params)
        self.message.content_subtype = "html"

    def attach(self, path: str, content_id: str):
        self.message.attach(attach_data(path, content_id))
        return self

    def attach_file(self, path: str, mimetype=None):
        self.message.attach_file(finders.find(path), mimetype)
        return self

    def send(self):
        return self.message.send()
