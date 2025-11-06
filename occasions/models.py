import uuid
from django.db import models
from django.conf import settings


class Occasion(models.Model):
    occasion_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    occasion_name = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    max_attendees = models.PositiveIntegerField()
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='occasions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'occasions'
        ordering = ['-date_time']

    def __str__(self):
        return self.occasion_name
