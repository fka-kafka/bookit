from rest_framework import serializers
from .models import Reservation


class RSVPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            'reservation_id',  'occasion', 'attendee', 'reserved_at', 'approved'
        ]
        read_only_fields = [
            'reserved_at', 'approved'
        ]
