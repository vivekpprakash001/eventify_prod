from django.urls import path
from . import views

app_name = 'master_data'

urlpatterns = [
    path('event-types/', views.EventTypeListView.as_view(), name='event_type_list'),
    path('event-types/add/', views.EventTypeCreateView.as_view(), name='event_type_add'),
    path('event-types/<int:pk>/edit/', views.EventTypeUpdateView.as_view(), name='event_type_edit'),
    path('event-types/<int:pk>/delete/', views.EventTypeDeleteView.as_view(), name='event_type_delete'),
]
