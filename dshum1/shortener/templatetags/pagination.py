import logging

from django import template

register = template.Library()
logger = logging.getLogger(__name__)


@register.simple_tag(takes_context=True)
def page_link(context, page: int = 1):
    request = context['request']
    temp_get = request.GET.copy()
    temp_get['page'] = page
    return '?' + '&'.join([f"{key}={value}" for key, value in temp_get.items()])
