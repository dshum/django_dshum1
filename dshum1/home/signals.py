from django import dispatch

user_registered = dispatch.Signal()
profile_changed = dispatch.Signal()
password_changed = dispatch.Signal()
