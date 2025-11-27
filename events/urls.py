from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('add/', views.EventCreateView.as_view(), name='event_add'),
    path('<int:pk>/edit/', views.EventUpdateView.as_view(), name='event_edit'),
    path('<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),

    path('<int:pk>/images/', views.event_images, name='event_images'),
    path('<int:pk>/images/add/', views.add_event_images, name='add_event_images'),
    path('<int:pk>/images/<int:img_id>/delete/', views.delete_event_image, name='delete_event_image'),
    path('<int:pk>/images/<int:img_id>/primary/', views.set_primary_image, name='set_primary_image'),
]
