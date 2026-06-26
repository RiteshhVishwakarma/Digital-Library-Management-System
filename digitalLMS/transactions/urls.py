from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('issue/', views.issue_book, name='issue_book'),
    path('list/', views.transaction_list, name='transaction_list'),
]
