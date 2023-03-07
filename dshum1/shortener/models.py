import hashlib
import logging
import random

from django.conf import settings
from django.db import models, IntegrityError
from django.db.models import F, Q
from django.urls import reverse


class TokenQuerySet(models.QuerySet):
    def recent(self, take: int = 10):
        return self.order_by('-created_at')[:take]

    def ordered(self):
        return self.order_by('-created_at')

    def full_url(self, full_url: str):
        return self.filter(full_url=full_url)

    def short_url(self, short_url: str):
        return self.filter(short_url=short_url)

    def search(self, query: str):
        return self.filter(Q(short_url__icontains=query) | Q(full_url__icontains=query)) if query else self

    def create_token(self, full_url: str, short_url: str = None, is_active: bool = True):
        return self.create(full_url=full_url, short_url=short_url, is_active=is_active)


class TokenManager(models.Manager):
    def get_queryset(self):
        return TokenQuerySet(self.model)

    def recent(self, take: int = 10):
        return self.get_queryset().recent(take=take)

    def ordered(self):
        return self.get_queryset().ordered()

    def full_url(self, full_url: str):
        return self.get_queryset().full_url(full_url=full_url)

    def short_url(self, short_url: str):
        return self.get_queryset().short_url(short_url=short_url)

    def search(self, query: str):
        return self.get_queryset().search(query=query)

    def update_counter(self, short_url: str):
        return self.get_queryset().filter(short_url=short_url) \
            .update(requests_count=F('requests_count') + 1)

    def create_token(self, full_url: str, short_url: str = None):
        if short_url:
            return self.get_queryset().create_token(full_url=full_url, short_url=short_url, is_active=True)
        else:
            while True:
                short_url = ''.join(random.sample(settings.CHARACTERS, 6))
                try:
                    return self.get_queryset().create_token(full_url=full_url, short_url=short_url, is_active=True)
                except IntegrityError:
                    pass


class Token(models.Model):
    full_url = models.URLField(max_length=1000, unique=True)
    short_url = models.CharField(max_length=20, unique=True, db_index=True)
    requests_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    tokens = TokenManager()

    def __repr__(self):
        return f"Token #{self.id}"

    def __str__(self) -> str:
        return f"{self.short_url} -> {self.full_url}"

    def get_absolute_url(self):
        return settings.BASE_URL + reverse('shortener.redirect', kwargs={'short_url': self.short_url})
