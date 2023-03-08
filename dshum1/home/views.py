from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from .forms import RegistrationForm, ProfileForm, PasswordForm


def is_guest(user):
    return user.is_anonymous


@cache_page(60 * 5)
@vary_on_cookie
def index(request):
    return render(request, 'index.html')


@user_passes_test(is_guest, login_url='home', redirect_field_name=None)
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(
                form.cleaned_data.get('password')
            )
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'home/register.html', {'form': form})


# @cache_page(60 * 5)
# @vary_on_cookie
@login_required
def home(request):
    recent_messages = request.user.messages.order_by('-created_at')[:10]
    return render(request, 'home/index.html', {'recent_messages': recent_messages})


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'home/profile.html', {'form': form})


@login_required
def password(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST, instance=request.user)
        if form.is_valid():
            request.user.set_password(
                form.cleaned_data.get('password')
            )
            request.user.save()
            return redirect('profile')
    else:
        form = PasswordForm(instance=request.user)
    return render(request, 'home/password.html', {'form': form})
