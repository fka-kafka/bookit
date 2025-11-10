from django.urls import path
from . import views

urlpatterns = [
    path('occasions/<uuid:occasion_id>/rsvp',
         views.make_reservation, name='rsvp'),
    path('occasions/reservations',
         views.get_reservations, name='get-reservations'),
]
