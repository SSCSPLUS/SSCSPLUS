from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path('admin/stats/', views.admin_stats_view, name='admin_stats'),
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('statement/', views.statement_view, name='statement'),
    path('ft/', views.ft_view, name='ft'),
    path('pin-change/', views.pin_change_view, name='pin_change'),
    path('api/user-lookup/', views.api_user_lookup, name='api_user_lookup'),
    path('transfer/', views.transfer_view, name='transfer'),
    path('logout/', views.logout_view, name='logout'),
]
