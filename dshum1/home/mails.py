from django.contrib.auth.models import User

from utils.mailable import Mailable


class RegisterMail(Mailable):
    def __init__(self, user: User):
        name = f"{user.first_name} {user.last_name}"
        super().__init__(
            subject="Your account has been created!",
            to=(name, user.email),
            template="home/mails/register.html",
            scope={"user": user}
        )


class EditProfileMail(Mailable):
    def __init__(self, user: User):
        name = f"{user.first_name} {user.last_name}"
        super().__init__(
            subject="Your profile has been updated",
            to=(name, user.email),
            template="home/mails/edit_profile.html",
            scope={"user": user}
        )


class ChangePasswordMail(Mailable):
    def __init__(self, user: User, new_password: str):
        name = f"{user.first_name} {user.last_name}"
        super().__init__(
            subject="Your password has been changed",
            to=(name, user.email),
            template="home/mails/change_password.html",
            scope={"user": user, "new_password": new_password}
        )
