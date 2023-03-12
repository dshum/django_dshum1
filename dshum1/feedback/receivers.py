from django.dispatch import receiver

from utils.mailable import Mailer
from .mails import MessageMail
from .models import Message
from .signals import message_received


@receiver(message_received)
def send_message_email(sender, message: Message, **kwargs):
    print(sender, message, kwargs)
    Mailer(MessageMail(message)).send()
