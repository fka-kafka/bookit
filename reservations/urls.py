from django.urls import path
from . import views

urlpatterns = [
    path('occasions/<uuid:occasion_id>/rsvp',
         views.make_reservation, name='rsvp'),
    path('occasions/<uuid:reservation_id>/approve',
         views.approve_reservation, name='approve-rsvp'),
]
