from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts.views import dashboard
from accounts.customer_views import RegisterView
from accounts.customer_views import login_view, logout_view, customer_dashboard
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path('dashboard/', customer_dashboard, name='customer_dashboard'),

    path('master-data/', include('master_data.urls')),
    path('events/', include('events.urls')),
    path('accounts/', include('accounts.urls')),
    path('api/', include('mobile_web_api.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
