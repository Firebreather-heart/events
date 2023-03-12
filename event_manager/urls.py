from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.admin_key,name='admin_key'),
    path('evm/<str:link>/', views.register, name='event_home'),
    path('create/', views.create, name='console'),
    path('', views.events, name='event_list'),
    path('<str:link>/edit/', views.edit_event, name='edit'),
    path('<str:link>/detail/', views.event_detail, name='event_detail'),
    path('<str:link>/speakers/', views.new_speaker, name='add_speaker'),
    path('<str:link>/partners/', views.new_partner, name='add_partner'),
    path('<str:link>/partner/<int:id>/delete/', views.remove_partner, name='del_p'),
    path('<str:link>/speaker/<int:id>/delete/', views.remove_speaker, name='del_s'),
    path('<str:link>/delete/', views.remove_event, name='event_del'),
    path('<str:link>/invites/', views.sendIv, name='invite')
]