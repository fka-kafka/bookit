from django.contrib import admin
from .models import Occasion


@admin.register(Occasion)
class OccasionAdmin(admin.ModelAdmin):
    list_display = ['occasion_name', 'location',
                    'date_time', 'max_attendees', 'organizer']
    list_filter = ['location', 'date_time']
    search_fields = ['occasion_name', 'location']
