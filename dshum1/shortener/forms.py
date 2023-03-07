from django import forms
from django.urls import reverse

from .models import Token


class CreateTokenForm(forms.Form):
    full_url = forms.URLField(label='Full URL', required=True)
    short_url = forms.CharField(label='Short URL (optional)', required=False, min_length=6, max_length=6)

    class Meta:
        model = Token
        fields = ('full_url', 'short_url')

    def clean_full_url(self):
        full_url = self.cleaned_data['full_url'].rstrip('/')
        if token := Token.tokens.full_url(full_url=full_url).first():
            raise forms.ValidationError(f"This URL already exists: {token.get_absolute_url()}")
        return full_url

    def clean_short_url(self):
        short_url = self.cleaned_data['short_url']
        if Token.tokens.short_url(short_url=short_url).exists():
            raise forms.ValidationError(f"This short URL already exists.")
        return short_url
