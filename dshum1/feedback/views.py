from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from .forms import CreateMessageForm
from .models import Message
from .signals import message_received


@cache_page(60 * 5)
@vary_on_cookie
def index(request):
    messages = Message.messages.recent()
    paginator = Paginator(messages, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'feedback/index.html', {'messages_page_obj': page_obj})


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
            message_received.send(sender='feedback_create_message', message=message)
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
