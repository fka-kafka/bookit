from rest_framework import serializers
from .models import Occasion


class OccasionSerializer(serializers.ModelSerializer):
    organizer_name = serializers.CharField(
        source='organizer.get_full_name', read_only=True)

    class Meta:
        model = Occasion
        fields = ['occasion_id', 'occasion_name', 'date_time',
                  'location', 'max_attendees', 'organizer_name', 'created_at']
        read_only_fields = ['occasion_id', 'created_at']
