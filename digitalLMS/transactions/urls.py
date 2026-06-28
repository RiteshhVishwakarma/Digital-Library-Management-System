from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('', views.transaction_list, name='transaction_list'),
    path('issue/', views.issue_book, name='issue_book'),
    path('<int:pk>/', views.transaction_detail, name='transaction_detail'),
    path('<int:pk>/return/', views.return_book, name='return_book'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
]
