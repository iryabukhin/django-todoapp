from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime


class HashTag(models.Model):
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)


class Todo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    priority = models.PositiveSmallIntegerField(blank=True, null=True)

    hashtags = models.ManyToManyField(HashTag)

    class Meta:
        ordering = ["-priority", "-created_at"]

    def is_overdue(self) -> bool:
        if not self.due_date:
            return False
        return datetime.now() > self.due_date

    # Auto set task completion datetime
    def save(self, **kwargs):
        if self.completed:
            self.completed_date = datetime.now()
        super(Todo, self).save()
