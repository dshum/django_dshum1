import random
import string
from pathlib import Path
from typing import Any, TypedDict, Optional, NamedTuple

from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string


class Address(NamedTuple):
    email: str
    name: Optional[str] = None

    def to_string(self):
        return f"{self.name} <{self.email}>" if self.name else self.email


def convert_address(address: Address | list[Address] = None):
    if address is None:
        return None
    addresses = address if isinstance(address, list) else [address]
    return [to.to_string() for to in addresses]


class Mailable:
    def __init__(self,
                 subject: str,
                 to: Address | list[Address],
                 template: str,
                 scope: dict[str: Any],
                 bcc: Address | list[Address] = None,
                 cc: Address | list[Address] = None,
                 from_email: Address = None,
                 reply_to: str = None,
                 headers: dict[str: str] = None):
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

    def attach(self, filename, path, mimetype=None):
        path = Path(path)
        with path.open('rb') as file:
            content = file.read()
            self.message.attach(filename, content, mimetype)
        return self

    def attach_file(self, path, mimetype=None):
        self.message.attach_file(path, mimetype)
        return self

    def send(self):
        return self.message.send()
