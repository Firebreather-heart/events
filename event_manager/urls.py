from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create, name='console'),
    path('events/', views.events, name='event_list')
]