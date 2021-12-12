from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime

class Todo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    priority = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        ordering = ["-priority", "-created_at"]

    def is_overdue(self) -> bool:
        if not self.due_date:
            return False
        return datetime.today().date() > self.due_date

    # Auto set task completion datetime
    def save(self, **kwargs):
        if self.completed:
            self.completed_at = timezone.now()
        super(Todo, self).save()

    def get_status_msg(self) -> str:
        if self.completed:
            return "Completed"
        if self.is_overdue():
            return "Overdue"
        return "In Progress"

    def get_absolute_url(self):
        return reverse("todo-edit", kwargs={'pk': self.pk})
