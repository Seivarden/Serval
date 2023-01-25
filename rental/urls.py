from django.urls import path, include 
from . import views

import rest_registration

app_name = 'rental'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('cars/', views.CarListView.as_view(), name='car-list'),
    path('car/<uuid:pk>', views.CarDetailView.as_view(), name='car-detail'),
    path('bookings/', views.BookingListView.as_view(), name='booking-list'),
    path('booking/<uuid:pk>', views.BookingDetailView.as_view(), name='booking-detail'),
    path('booking/create', views.BookingCreate.as_view(), name='booking-create'),
    path('clients/', views.UserListView.as_view(), name='customer-list'),
    path('client/<uuid:pk>', views.UserDetailView.as_view(), name='user-detail'),    
    path('Estates/', views.GeneralListView.as_view(), name='general-list'),
]