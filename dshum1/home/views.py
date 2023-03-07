from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie


@cache_page(60 * 5)
@vary_on_cookie
@login_required
def home(request):
    recent_messages = request.user.messages.order_by('-created_at')[:10]
    return render(request, 'home/index.html', {'recent_messages': recent_messages})
