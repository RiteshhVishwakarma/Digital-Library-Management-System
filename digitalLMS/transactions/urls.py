from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('', views.transaction_list, name='transaction_list'),
    path('issue/', views.issue_book, name='issue_book'),
    path('<int:pk>/', views.transaction_detail, name='transaction_detail'),
]
