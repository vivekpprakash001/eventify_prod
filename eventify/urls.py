from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts.views import dashboard
from accounts.views import login_view
from accounts.views import logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('dashboard/', dashboard, name='dashboard'),

    path('master-data/', include('master_data.urls')),
    path('events/', include('events.urls')),
    path('accounts/', include('accounts.urls')),
]
