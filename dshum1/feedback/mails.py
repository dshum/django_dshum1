from django.contrib.auth.models import User

from .models import Message
from utils.mailable import Mailable, Address


class MessageMail(Mailable):
    def __init__(self, message: Message):
        super().__init__(
            subject="New message",
            to=Address(name='Denis', email='denis-shumeev@yandex.ru'),
            template="feedback/mails/message.html",
            scope={"message": message}
        )
