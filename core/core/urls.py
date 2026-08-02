"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('pricing/', views.PricingView.as_view(), name='pricing'),
    path('accounts/', include('allauth.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('workspace/', include('workspace.urls')),
    path('settings/', include(('dashboard.settings_urls', 'dashboard_settings'), namespace='settings')),
    path('billing/', include('billing.urls')),
    path('copilot/', include('copilot.urls')),
]
