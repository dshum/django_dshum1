from django.apps import AppConfig
from django.db.models.signals import post_save, pre_save


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        from .receivers import (
            send_register_mail,
            send_edit_profile_mail,
            send_change_password_mail,
        )
