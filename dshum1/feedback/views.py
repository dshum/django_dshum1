from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from utils.mailable import Mailer
from .forms import CreateMessageForm
from .mails import MessageMail
from .models import Message


@cache_page(60 * 5)
@vary_on_cookie
def index(request):
    recent_messages = Message.messages.recent()
    return render(request, 'feedback/index.html', {'recent_messages': recent_messages})


def create(request):
    if request.method == 'POST':
        form = CreateMessageForm(request.POST)
        if form.is_valid():
            message = Message.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message'],
                is_human=form.cleaned_data['is_human'],
                user=request.user,
            )
            Mailer(MessageMail(message)).send()
            messages.add_message(request, messages.SUCCESS, 'Your message has been sent!')
            return redirect('feedback.create')
    elif request.user.is_authenticated:
        form = CreateMessageForm(initial={
            'name': request.user.first_name + ' ' + request.user.last_name,
            'email': request.user.email,
        })
    else:
        form = CreateMessageForm()

    return render(request, 'feedback/create.html', {'form': form})
