from django import forms
from django.urls import reverse

from .models import Message


class CreateMessageForm(forms.ModelForm):
    name = forms.CharField(label='Name', required=True, max_length=100)
    email = forms.EmailField(label='Email (optional)', required=False, help_text='We will not give your email to anyone')
    message = forms.CharField(label='Message', required=True, widget=forms.Textarea)
    is_human = forms.BooleanField(label='Are you a human?', required=False, help_text='Confirm that you are not a robot')

    class Meta:
        model = Message
        fields = ('name', 'email', 'message', 'is_human')
