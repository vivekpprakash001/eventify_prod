from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
# from accounts.views import dashboard, login_view, logout_view, UserListView, UserCreateView, UserUpdateView, UserDeleteView
# from accounts.customer_views import RegisterView
# from accounts.customer_views import login_view, logout_view, customer_dashboard, customer_calendar
# from accounts.customer_views import customer_profile
from accounts import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("", login_view, name="login"),
    # path("logout/", logout_view, name="logout"),
    # path("register/", RegisterView.as_view(), name="register"),
    # path('dashboard/', customer_dashboard, name='customer_dashboard'),
    # path('calendar/', customer_calendar, name='customer_calendar'),
    # path('profile/', customer_profile, name='customer_profile'),


    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/add/', views.UserCreateView.as_view(), name='user_add'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),

    path('master-data/', include('master_data.urls')),
    path('events/', include('events.urls')),
    path('accounts/', include('accounts.urls')),
    path('api/', include('mobile_api.urls')),
    # path('web-api/', include('web_api.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
