from django.db import models
from datetime import datetime


class Task(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    due_date = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    completed_date = models.BooleanField(default=False)

    prioriy = models.PositiveSmallIntegerField(blank=True, null=True)

    def is_overdue(self) -> bool:
        if not self.due_date:
            return False
        return datetime.now() > self.due_date

    # Auto set task completion datetime
    def save(self, **kwargs):
        if self.completed:
            self.completed_date = datetime.now()
        super(Task, self).save()

    class Meta:
        ordering = ['-priority', '-created_at']

