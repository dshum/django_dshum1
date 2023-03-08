from django import forms
from django.contrib.auth.models import User
from django.urls import reverse


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Login', required=True, max_length=100)
    password = forms.CharField(label='Password', required=True, max_length=50,
                               widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm password', required=True, max_length=50,
                                       widget=forms.PasswordInput)
    first_name = forms.CharField(label='First name', required=True, max_length=100)
    last_name = forms.CharField(label='Last name', required=True, max_length=100)
    email = forms.EmailField(label='Email', required=True,
                             help_text='We will not give your email to anyone')
    is_human = forms.BooleanField(label='Are you a human?', required=True,
                                  help_text='Confirm that you are not a robot')

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'first_name', 'last_name', 'email')

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords must match")
        return confirm_password


class ProfileForm(forms.ModelForm):
    username = forms.CharField(label='Login', required=True, max_length=100)
    first_name = forms.CharField(label='First name', required=True, max_length=100)
    last_name = forms.CharField(label='Last name', required=True, max_length=100)
    email = forms.EmailField(label='Email', required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class PasswordForm(forms.ModelForm):
    current_password = forms.CharField(label='Current password', required=True, max_length=50,
                                       widget=forms.PasswordInput)
    password = forms.CharField(label='New password', required=True, max_length=50,
                               widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm password', required=True, max_length=50,
                                       widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('current_password', 'password', 'confirm_password')

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.instance.check_password(current_password):
            raise forms.ValidationError("Wrong current password")
        return current_password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords must match")
        return confirm_password
