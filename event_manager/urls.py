from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.admin_key,name='admin_key'),
    path('evm/<str:link>/', views.register, name='event_home'),
    path('create/', views.create, name='console'),
    path('', views.events, name='event_list'),
    path('console/<str:link>/edit/', views.edit_event, name='edit'),
    path('console/<str:link>/', views.event_detail, name='event_detail'),
    path('console/<str:link>/speakers/', views.new_speaker, name='add_speaker'),
    path('console/<str:link>/partners/', views.new_partner, name='add_partner'),
    path('console/<str:link>/partner/<int:id>/delete/', views.remove_partner, name='del_p'),
    path('console/<str:link>/speaker/<int:id>/delete/', views.remove_speaker, name='del_s'),
    path('console/<str:link>/delete/', views.remove_event, name='event_del'),
    path('console/<str:link>/invites/', views.sendIv, name='invite')
]