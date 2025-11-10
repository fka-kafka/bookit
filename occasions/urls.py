from django.urls import path
from . import views

urlpatterns = [
    path('occasions/', views.occasion_list, name='occasion-list'),
    path('occasions/<uuid:occasion_id>',
         views.occasion_detail, name='occasion-detail'),
]
