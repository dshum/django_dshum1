from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from .forms import RegistrationForm


@cache_page(60 * 5)
@vary_on_cookie
def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(
                form.cleaned_data.get('password')
            )
            user.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'home/register.html', {'form': form})


@cache_page(60 * 5)
@vary_on_cookie
@login_required
def home(request):
    recent_messages = request.user.messages.order_by('-created_at')[:10]
    return render(request, 'home/index.html', {'recent_messages': recent_messages})
