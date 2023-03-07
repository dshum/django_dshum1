import logging

from django import forms
from django.conf import settings
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import RedirectView

from .forms import CreateTokenForm
from .models import Token

logger = logging.getLogger(__name__)


@cache_page(60 * 5)
@vary_on_cookie
def index(request):
    query = request.GET.get('query', "")
    tokens = Token.tokens.search(query=query).ordered()
    paginator = Paginator(tokens, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shortener/index.html', {'query': query, 'tokens_page_obj': page_obj})


def create(request):
    if request.method == 'POST':
        form = CreateTokenForm(request.POST)
        if form.is_valid():
            Token.tokens.create_token(
                full_url=form.cleaned_data['full_url'],
                short_url=form.cleaned_data['short_url'],
            )
            return redirect('shortener.index')
    else:
        form = CreateTokenForm()

    return render(request, 'shortener/create.html', {'form': form})


@cache_page(60 * 5)
def redirect_url(request, short_url):
    token = Token.tokens.short_url(short_url=short_url).first()
    if token:
        Token.tokens.update_counter(short_url=token.short_url)
        return redirect(token.full_url)
    else:
        return render(request, 'shortener/not_found.html', {'short_url': short_url})
