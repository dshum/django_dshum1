from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from .forms import RegistrationForm


def is_guest(user):
    return user.is_anonymous


@cache_page(60 * 5)
@vary_on_cookie
def index(request):
    return render(request, 'index.html')


@user_passes_test(is_guest, login_url='home.index', redirect_field_name=None)
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
            return redirect('home.index')
    else:
        form = RegistrationForm()

    return render(request, 'home/register.html', {'form': form})


# @cache_page(60 * 5)
# @vary_on_cookie
@login_required
def home(request):
    recent_messages = request.user.messages.order_by('-created_at')[:10]
    return render(request, 'home/index.html', {'recent_messages': recent_messages})
