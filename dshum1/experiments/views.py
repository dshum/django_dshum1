import logging

from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

logger = logging.getLogger(__name__)


@cache_page(60 * 5)
@vary_on_cookie
def index(request):
    return render(request, 'index.html')


@cache_page(60 * 5)
@vary_on_cookie
def drama(request):
    result = get_drama_problem_result()
    return render(request, 'drama.html', {'result': result})


def get_drama_problem_result():
    digits = range(0, 10)
    return [{"drama": (D, R, A, M, A), "teatr": (T, E, A, T, R)}
            for D in range(1, 10)
            for R in digits
            for A in digits
            for M in digits
            for T in range(1, 10)
            for E in digits
            if D != R != A != M != T != E
            and 2 * (D * 10000 + R * 1000 + A * 100 + M * 10 + A) == T * 10000 + E * 1000 + A * 100 + T * 10 + R]


# def handler404(request, exception, template_name='404.html'):
#     response = render(request, template_name)
#     response.status_code = 404
#     return response


# def handler500(request, exception, template_name='500.html'):
#     response = render(request, template_name)
#     response.status_code = 500
#     return response
