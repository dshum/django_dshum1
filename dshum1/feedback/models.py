from django.contrib.auth.models import User
from django.db import models


class MessageQuerySet(models.QuerySet):
    def recent(self, take: int = 10):
        return self.order_by('-created_at')[:take]


class MessageManager(models.Manager):
    def get_queryset(self):
        return MessageQuerySet(self.model)

    def recent(self, take: int = 10):
        return self.get_queryset().recent(take=take)


class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    message = models.TextField()
    is_human = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        null=True,
        blank=True,
        default=None,
        related_name='messages'
    )

    def __repr__(self) -> str:
        return f"Message #{self.id}"

    def __str__(self) -> str:
        return f"{self.message}"

    objects = models.Manager()
    messages = MessageManager()
