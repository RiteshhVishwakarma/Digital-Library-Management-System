from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('cd cd cd/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
