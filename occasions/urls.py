from django.urls import path
from . import views

urlpatterns = [
    path('', views.occasion_list, name='occasion-list'),
    path('<uuid:occasion_id>', views.occasion_detail, name='occasion-detail'),
]
