from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import CreateLinkForm
from .models import Link


def index(request):
    query = request.GET.get('query')
    links = Link.links.search(query=query)
    paginator = Paginator(links, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'links/index.html', {'query': query, 'links': page_obj})


def create(request):
    if request.method == 'POST':
        form = CreateLinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.user = request.user
            link.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, 'New link has been added!')
            return redirect('links.index')
    else:
        form = CreateLinkForm()

    return render(request, 'links/create.html', {'form': form})
