from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('torts/', views.BookListView.as_view(), name='torts'),
    path('tort/<int:pk>', views.TortDetailView.as_view(), name='tort-detail'),
    path('konditers/', views.KonditerListView.as_view(), name='konditers'),
    path('konditer/<int:pk>', views.KonditerDetailView.as_view(), name='konditer-detail'),
]
urlpatterns += [   
    path('mytorts/', views.LoanedTortsByUserListView.as_view(), name='my-borrowed'),
]
urlpatterns += [   
    path('tort/<uuid:pk>/renew/', views.renew_tort_librarian, name='renew-tort-librarian'),
]