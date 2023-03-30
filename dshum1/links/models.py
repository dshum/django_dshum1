from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


class LinkTag(models.Model):
    title = models.CharField(max_length=50, default=None)

    class Meta:
        ordering = ['title']

    def __str__(self) -> str:
        return self.title


class LinksQuerySet(models.QuerySet):
    def search(self, query: str):
        return self.filter(Q(title__icontains=query) | Q(url__icontains=query)) if query else self


class LinksManager(models.Manager):
    def get_queryset(self):
        return LinksQuerySet(self.model)

    def search(self, query: str):
        return self.get_queryset().search(query=query)


class Link(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(LinkTag, related_name='links')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='links'
    )

    class Meta:
        ordering = ['-id']

    def __str__(self) -> str:
        return self.url

    objects = models.Manager()
    links = LinksManager()
