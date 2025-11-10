import uuid
from django.db import models
from django.conf import settings
from occasions.models import Occasion


class Reservation(models.Model):
    reservation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    occasion = models.ForeignKey(
        Occasion,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    attendee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    approved = models.BooleanField(default=False)
    reserved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reservations'
        unique_together = ('occasion', 'attendee')
        ordering = ['-reserved_at']

    def __str__(self):
        return f'{self.attendee.get_full_name()} reserved {self.occasion.occasion_name}'
