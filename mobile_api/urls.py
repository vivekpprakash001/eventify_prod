from django.urls import path
from .views import *


# User URLS
urlpatterns = [
    path('user/register/', RegisterView.as_view(), name='json_register'),
    path('user/login/', LoginView.as_view(), name='json_login'),
    path('user/status/', StatusView.as_view(), name='user_status'),
    path('user/logout/', LogoutView.as_view(), name='user_logout'),
]

# Event URLS

urlpatterns += [
    path('events/type-list/', EventTypeListAPIView.as_view()),
    path('events/pincode-events/', EventListAPI.as_view()),
    path('events/event-details/', EventDetailAPI.as_view()),
    path('events/event-images/', EventImagesListAPI.as_view()),
    path('events/events-by-category/', EventsByCategoryAPI.as_view(), name='api_events_by_category'),
    path('events/events-by-month-year/', EventsByMonthYearAPI.as_view(), name='events_by_month_year'),
    path('events/events-by-date/', EventsByDateAPI.as_view(), name='events_by_date'),
]
