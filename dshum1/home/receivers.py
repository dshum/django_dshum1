from django.contrib.auth.models import User
from django.dispatch import receiver

from utils.mailable import Mailer
from .mails import RegisterMail, EditProfileMail, ChangePasswordMail
from .signals import user_registered, profile_changed, password_changed


@receiver(user_registered)
def send_register_mail(sender, user: User, **kwargs):
    Mailer(RegisterMail(user)) \
        .attach('mainecoon.jpg', 'logo') \
        .send()


@receiver(profile_changed)
def send_edit_profile_mail(sender, user: User, **kwargs):
    Mailer(EditProfileMail(user)) \
        .attach('mainecoon.jpg', 'logo') \
        .send()


@receiver(password_changed)
def send_change_password_mail(sender, user: User, new_password: str, **kwargs):
    Mailer(ChangePasswordMail(user, new_password=new_password)) \
        .attach('mainecoon.jpg', 'logo') \
        .send()
